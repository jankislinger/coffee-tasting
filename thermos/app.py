import yaml
from flask import Flask, render_template, url_for

app = Flask(__name__)

# Base path for the repository (update this with your repository name)
BASE_PATH = "/<repository-name>"


# Helper to prepend base path to URLs
def full_url(endpoint, **kwargs):
    return BASE_PATH + url_for(endpoint, **kwargs)


# Load YAML data
def load_yaml(file_path):
    with open(file_path) as file:
        return yaml.safe_load(file)


# Mock data loaded from YAML files
# roasteries = load_yaml("data/roasteries.yaml")
# coffees = load_yaml("data/coffees.yaml")
# users = load_yaml("data/users.yaml")


# Routes
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/coffees")
def coffees():
    top_rated_coffees = sorted(coffees, key=lambda x: -x["average_rating"])[:5]
    return render_template(
        "index.html",
        top_rated_coffees=top_rated_coffees,
        roasteries=roasteries,
        full_url=full_url,
    )


@app.route("/roastery/<name>/")
def roastery(name):
    roastery_coffees = [c for c in coffees if c["roastery"] == name]
    return render_template(
        "roastery.html",
        name=name,
        coffees=roastery_coffees,
        full_url=full_url,
    )


@app.route("/coffee/<int:coffee_id>/")
def coffee(coffee_id):
    # coffee = next((c for c in coffees if c["id"] == id), None)
    # if not coffee:
    #     return "Coffee not found", 404
    # ratings = coffee.get("ratings", [])
    return render_template(
        "coffee.html",
        # coffee=coffee,
        # ratings=ratings,
        # full_url=full_url,
    )


@app.route("/user/<username>/")
def user(username):
    user_data = next((u for u in users if u["username"] == username), None)
    if not user_data:
        return "User not found", 404
    user_ratings = user_data.get("ratings", [])
    return render_template(
        "user.html",
        username=username,
        ratings=user_ratings,
        full_url=full_url,
    )


if __name__ == "__main__":
    app.run(debug=True)
