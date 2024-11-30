#!/usr/bin/env python3

import glob
import os

import yaml
from pydantic import ValidationError

from coffee_tasting.data_models import (
    CoffeeBean,
    Participant,
    ParticipantRanking,
    ParticipantRating,
)


def load_yaml_file(file_path):
    with open(file_path, "r") as f:
        data = yaml.safe_load(f)
    return data


def main():
    errors = []
    coffee_ids = set()
    participant_ids = set()

    # Load and validate coffee beans
    coffee_files = glob.glob("data/coffees/*.yaml")
    coffees = {}
    for file in coffee_files:
        data = load_yaml_file(file)
        try:
            coffee = CoffeeBean(**data)
            coffees[coffee.coffee_id] = coffee
            coffee_ids.add(coffee.coffee_id)
        except ValidationError as e:
            errors.append(f"Error in {file}:\n{e}")

    # Load and validate participants
    participant_files = glob.glob("data/participants/*.yaml")
    participants = {}
    for file in participant_files:
        data = load_yaml_file(file)
        try:
            participant = Participant(**data)
            participants[participant.participant_id] = participant
            participant_ids.add(participant.participant_id)
        except ValidationError as e:
            errors.append(f"Error in {file}:\n{e}")

    # Load and validate session ratings and rankings
    session_dirs = glob.glob("data/sessions/*")
    for session_dir in session_dirs:
        session_date = os.path.basename(session_dir)

        # Validate ratings
        rating_files = glob.glob(os.path.join(session_dir, "ratings", "*.yaml"))
        for file in rating_files:
            data = load_yaml_file(file)
            try:
                participant_rating = ParticipantRating(**data)
                # Validate participant ID
                if participant_rating.participant_id not in participant_ids:
                    errors.append(
                        f'Invalid participant_id "{participant_rating.participant_id}" in {file}'
                    )
                # Validate session date consistency
                if participant_rating.session_date != session_date:
                    errors.append(
                        f'Session date mismatch in {file}: Expected "{session_date}", found "{participant_rating.session_date}"'
                    )
                # Validate coffee IDs in ratings
                for rating in participant_rating.ratings:
                    if rating.coffee_id not in coffee_ids:
                        errors.append(f'Invalid coffee_id "{rating.coffee_id}" in {file}')
            except ValidationError as e:
                errors.append(f"Error in {file}:\n{e}")

        # Validate rankings
        ranking_files = glob.glob(os.path.join(session_dir, "rankings", "*.yaml"))
        for file in ranking_files:
            data = load_yaml_file(file)
            try:
                participant_ranking = ParticipantRanking(**data)
                # Validate participant ID
                if participant_ranking.participant_id not in participant_ids:
                    errors.append(
                        f'Invalid participant_id "{participant_ranking.participant_id}" in {file}'
                    )
                # Validate session date consistency
                if participant_ranking.session_date != session_date:
                    errors.append(
                        f'Session date mismatch in {file}: Expected "{session_date}", found "{participant_ranking.session_date}"'
                    )
                # Validate coffee IDs and ranks in rankings
                ranks = set()
                coffee_id_set = set()
                for ranking in participant_ranking.rankings:
                    if ranking.coffee_id not in coffee_ids:
                        errors.append(f'Invalid coffee_id "{ranking.coffee_id}" in {file}')
                    if ranking.rank in ranks:
                        errors.append(f'Duplicate rank "{ranking.rank}" in {file}')
                    else:
                        ranks.add(ranking.rank)
                    if ranking.coffee_id in coffee_id_set:
                        errors.append(
                            f'Duplicate coffee_id "{ranking.coffee_id}" in rankings of {file}'
                        )
                    else:
                        coffee_id_set.add(ranking.coffee_id)
            except ValidationError as e:
                errors.append(f"Error in {file}:\n{e}")

    # Report validation results
    if errors:
        print("Validation failed with the following errors:")
        for error in errors:
            print(f"- {error}\n")
        exit(1)
    else:
        print("All data validated successfully.")


if __name__ == "__main__":
    main()
