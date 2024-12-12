from pathlib import Path

from flask_frozen import Freezer

from app import app

app.config["FREEZER_BASE_URL"] = "/coffee-tasting"
freezer = Freezer(app)


@freezer.register_generator
def coffee():
    yield {"coffee_id": "doubleshot-farm-colombia-el-naranjo"}


if __name__ == "__main__":
    freezer.freeze()
    index_html = Path("build") / "index.html"
    assert "coffee-tasting/static" in index_html.read_text()
