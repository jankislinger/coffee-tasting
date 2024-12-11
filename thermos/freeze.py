from flask_frozen import Freezer

from app import app

app.config["FREEZER_BASE_URL"] = "https://example.com/mysite"
freezer = Freezer(app)


@freezer.register_generator
def coffee():
    yield {"coffee_id": "doubleshot-farm-colombia-el-naranjo"}


if __name__ == "__main__":
    freezer.freeze()
