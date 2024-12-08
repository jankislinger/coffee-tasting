from pathlib import Path

from flask_frozen import Freezer

from app import app

app.config["FREEZER_BASE_URL"] = "/coffee-tasting"
freezer = Freezer(app)
DATA_PATH = Path(__file__).parents[1] / "data"
print(DATA_PATH)
assert DATA_PATH.is_dir()


@freezer.register_generator
def coffee():
    for path in DATA_PATH.joinpath("coffees").glob("*.yaml"):
        yield {"coffee_id": path.stem}


if __name__ == "__main__":
    freezer.freeze()
    index_html = Path("build") / "index.html"
    assert "coffee-tasting/static" in index_html.read_text()
