import glob
import os
import sys
from pathlib import Path
from typing import Container, Any

import yaml
from pydantic import ValidationError

from coffee_tasting.data_models import (
    Coffee,
    ParticipantRanking,
)

DATA_ROOT = Path(__file__).parents[2] / "data"


def main() -> int:
    errors = []

    coffees = validate_coffees()
    participants = validate_participants(errors)
    validate_sessions(coffees, participants, errors)

    # Report validation results
    if not errors:
        print("All data validated successfully.")
        return 0

    print(f"Validation failed with the following errors ({len(errors)}):")
    for error in errors:
        print(f"- {error}\n")
    return 1


def validate_coffees() -> dict[str, Coffee]:
    coffee_files = DATA_ROOT.joinpath("coffees").glob("*.yaml")
    coffees = {}
    for file in coffee_files:
        data = load_yaml_file(file)
        coffee = Coffee(**data)
        assert coffee.coffee_id == file.stem, "Coffee ID has to match file name"
        coffees[coffee.coffee_id] = coffee
    return coffees


def validate_participants(errors: list[str]) -> set[str]:
    try:
        participants = load_yaml_file(DATA_ROOT / "participants.yaml")
    except (ValidationError, FileNotFoundError) as e:
        errors.append(f"Failed to load yaml file for participants: {e}")
        return set()

    num_participants = len(participants)
    participants = set(participants)
    if len(participants) != num_participants:
        errors.append("Some participants are duplicated")
    return participants


def validate_sessions(
        coffee_ids: Container[str], participant_ids: Container[str], errors: list[str]
):
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


def load_yaml_file(file_path: Path | str) -> dict[str, Any] | list[Any]:
    if isinstance(file_path, str):
        file_path = Path(file_path)
    with file_path.open("r") as f:
        return yaml.safe_load(f)


def id_from_file_name(file_name: str) -> str:
    return file_name.split("/")[-1].rsplit(".", 1)[0]


if __name__ == "__main__":
    sys.exit(main())
