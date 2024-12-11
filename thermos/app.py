from pathlib import Path
from typing import Any

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
    )


def load_coffee(coffee_id: str) -> Coffee:
    data = load_yaml(DATA_DIR / "coffees" / f"{coffee_id}.yaml")
    return Coffee(**data)


if __name__ == "__main__":
    app.run(debug=True)
