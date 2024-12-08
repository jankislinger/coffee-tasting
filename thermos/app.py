from functools import cache
from pathlib import Path
from typing import Any

import polars as pl
import yaml
from coffee_tasting.data_models import Coffee
from flask import Flask, render_template

app = Flask(__name__)

DATA_DIR = Path(__file__).parent.parent / "data"


def load_yaml(file_path: Path) -> dict[str, Any]:
    with file_path.open() as file:
        return yaml.safe_load(file)


# Routes
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/coffee/<coffee_id>/")
def coffee(coffee_id: str):
    return render_template(
        "coffee.html",
        coffee=load_coffee(coffee_id),
        stats=load_coffee_stats(coffee_id),
        ratings=load_coffee_ratings(coffee_id),
    )


def load_coffee_stats(coffee_id: str) -> dict[str, str]:
    ratings = load_ratings().filter(pl.col("coffee_id").eq(coffee_id))
    if ratings.is_empty():
        return {
            "average_rating": "-",
            "session_count": "0",
            "most_frequent_rank": "-",
        }

    stats = ratings.select(
        average_rating=pl.col("rating").struct.field("overall").mean(),
        session_count=pl.col("session_date").n_unique(),
        most_frequent_rank=pl.col("rank").mode(),
    )
    assert stats.shape[0] == 1
    return stats.to_dicts()[0]


def load_coffee_ratings(coffee_id: str) -> list[dict]:
    return (
        load_ratings()
        .filter(pl.col("coffee_id").eq(coffee_id))
        .sort("session_date", "participant_id", descending=[True, False])
        .select(
            participant="participant_id",
            session="session_date",
            rank="rank",
            rating=pl.col("rating").struct.field("overall"),
        )
        .to_dicts()
    )


def load_coffee(coffee_id: str) -> Coffee:
    data = load_yaml(DATA_DIR / "coffees" / f"{coffee_id}.yaml")
    return Coffee(**data)


@cache
def load_ratings() -> pl.DataFrame:
    out = []
    for file in DATA_DIR.joinpath("sessions").glob("ratings/*.yaml"):
        data = load_yaml(file)
        rankings = data.pop("rankings")
        for ranking in rankings:
            out.append(data | ranking)
    return pl.DataFrame(out)


if __name__ == "__main__":
    app.run(debug=True)
