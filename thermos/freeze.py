from flask_frozen import Freezer
from app import app

freezer = Freezer(app)


@freezer.register_generator
def coffee():
    yield {"coffee_id": 0}


if __name__ == "__main__":
    freezer.freeze()
