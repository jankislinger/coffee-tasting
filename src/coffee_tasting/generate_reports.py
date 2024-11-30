#!/usr/bin/env python3

import glob
import os

import pandas as pd
import yaml
from jinja2 import Environment, FileSystemLoader

# Directories
DATA_DIR = "data"
COFFEES_DIR = os.path.join(DATA_DIR, "coffees")
PARTICIPANTS_DIR = os.path.join(DATA_DIR, "participants")
SESSIONS_DIR = os.path.join(DATA_DIR, "sessions")
TEMPLATES_DIR = "templates"
REPORTS_DIR = "reports"

# Ensure the reports directory exists
os.makedirs(REPORTS_DIR, exist_ok=True)


def load_yaml_files(directory):
    data = {}
    for file_path in glob.glob(os.path.join(directory, "*.yaml")):
        with open(file_path, "r") as f:
            content = yaml.safe_load(f)
            data[content.get("coffee_id") or content.get("participant_id")] = content
    return data


def generate_report_for_session(session_date):
    print(f"Generating report for session {session_date}...")

    # Load data
    coffees = load_yaml_files(COFFEES_DIR)
    participants = load_yaml_files(PARTICIPANTS_DIR)

    session_dir = os.path.join(SESSIONS_DIR, session_date)
    ratings_dir = os.path.join(session_dir, "ratings")
    rankings_dir = os.path.join(session_dir, "rankings")

    # Load ratings
    all_ratings = []
    for file_path in glob.glob(os.path.join(ratings_dir, "*.yaml")):
        with open(file_path, "r") as f:
            content = yaml.safe_load(f)
            participant_id = content["participant_id"]
            participant_name = participants.get(participant_id, {}).get("name", participant_id)
            for rating in content["ratings"]:
                rating["participant_id"] = participant_id
                rating["participant_name"] = participant_name
                all_ratings.append(rating)

    # Load rankings
    all_rankings = []
    for file_path in glob.glob(os.path.join(rankings_dir, "*.yaml")):
        with open(file_path, "r") as f:
            content = yaml.safe_load(f)
            participant_id = content["participant_id"]
            for ranking in content["rankings"]:
                ranking["participant_id"] = participant_id
                all_rankings.append(ranking)

    # Process data using pandas
    ratings_df = pd.DataFrame(all_ratings)
    rankings_df = pd.DataFrame(all_rankings)

    # Prepare data for the template
    rating_attributes = [
        "sweetness",
        "acidity",
        "bitterness",
        "body",
        "aroma",
        "flavor",
        "aftertaste",
    ]
    coffees_list = []

    for coffee_id, coffee in coffees.items():
        coffee_ratings = ratings_df[ratings_df["coffee_id"] == coffee_id]
        if not coffee_ratings.empty:
            # Calculate average ratings
            average_ratings = coffee_ratings[rating_attributes].mean().to_dict()
            # Convert individual ratings to a list of dictionaries
            individual_ratings = coffee_ratings.to_dict("records")
            # Add participant names
            # Prepare coffee data
            coffee_data = {
                "coffee_id": coffee_id,
                "name": coffee["name"],
                "origin": coffee["origin"],
                "roaster": coffee["roaster"],
                "roast_date": coffee["roast_date"],
                "roast_level": coffee["roast_level"],
                "flavor_notes": coffee["flavor_notes"],
                "average_ratings": average_ratings,
                "ratings": individual_ratings,
            }
            coffees_list.append(coffee_data)

    # Calculate overall rankings
    if not rankings_df.empty:
        # Convert ranks to numeric
        rankings_df["rank"] = pd.to_numeric(rankings_df["rank"], errors="coerce")
        # Calculate average rank for each coffee
        avg_rankings = rankings_df.groupby("coffee_id")["rank"].mean().reset_index()
        # Merge with coffee names
        avg_rankings["coffee_name"] = avg_rankings["coffee_id"].map(
            lambda cid: coffees.get(cid, {}).get("name", cid)
        )
        # Sort by average rank
        avg_rankings = avg_rankings.sort_values("rank")
        overall_rankings = avg_rankings.to_dict("records")
    else:
        overall_rankings = []

    # Load participant names
    participant_list = []
    for participant_id, participant in participants.items():
        if participant_id in ratings_df["participant_id"].unique():
            participant_list.append(
                {"participant_id": participant_id, "name": participant.get("name", participant_id)}
            )

    # Render the HTML template
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template("report_template.html")
    html_content = template.render(
        session_date=session_date,
        coffees=coffees_list,
        participants=participant_list,
        rating_attributes=rating_attributes,
        overall_rankings=overall_rankings,
    )

    # Save the HTML report
    output_file = os.path.join(REPORTS_DIR, f"{session_date}.html")
    with open(output_file, "w") as f:
        f.write(html_content)

    print(f"Report saved to {output_file}")


def main():
    # Find all sessions
    session_dirs = glob.glob(os.path.join(SESSIONS_DIR, "*"))
    session_dates = [os.path.basename(sdir) for sdir in session_dirs]

    for session_date in session_dates:
        generate_report_for_session(session_date)


if __name__ == "__main__":
    main()
