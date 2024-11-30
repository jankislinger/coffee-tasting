#!/usr/bin/env python3

import os
import random
import yaml
from datetime import datetime, timedelta
from typing import List
from coffee_tasting.data_models import (
    CoffeeBean,
    Participant,
    Rating,
    ParticipantRating,
    Ranking,
    ParticipantRanking,
)

# Constants
DATA_DIR = 'data'
COFFEES_DIR = os.path.join(DATA_DIR, 'coffees')
PARTICIPANTS_DIR = os.path.join(DATA_DIR, 'participants')
SESSIONS_DIR = os.path.join(DATA_DIR, 'sessions')

# Ensure directories exist
os.makedirs(COFFEES_DIR, exist_ok=True)
os.makedirs(PARTICIPANTS_DIR, exist_ok=True)
os.makedirs(SESSIONS_DIR, exist_ok=True)

# Generate 8 unique participants
participant_names = [
    'Alice Smith',
    'Bob Johnson',
    'Carol Williams',
    'David Jones',
    'Eve Brown',
    'Frank Miller',
    'Grace Davis',
    'Henry Wilson',
]

participant_ids = []
participants = []

for name in participant_names:
    participant_id = f"participant_{name.lower().replace(' ', '_')}"
    participant = Participant(
        participant_id=participant_id,
        name=name,
        email=f"{name.lower().replace(' ', '.')}@example.com",
        preferences=random.sample(
            ['Fruity', 'Nutty', 'Chocolatey', 'Floral', 'Citrus', 'Spicy'], 2
        ),
    )
    participants.append(participant)
    participant_ids.append(participant_id)

    # Save participant data
    participant_file = os.path.join(PARTICIPANTS_DIR, f"{participant_id}.yaml")
    with open(participant_file, 'w') as f:
        yaml.safe_dump(participant.model_dump(), f)

# Generate 5 coffees
coffee_names = [
    'Ethiopian Yirgacheffe',
    'Colombian Supremo',
    'Kenyan AA',
    'Guatemala Antigua',
    'Sumatra Mandheling',
]

coffee_ids = []
coffees = []

for name in coffee_names:
    coffee_id = f"coffee_{name.lower().replace(' ', '_').replace('/', '_')}"
    coffee = CoffeeBean(
        coffee_id=coffee_id,
        name=name,
        origin=name.split(' ')[0],
        roaster='Best Beans Co.',
        roast_date=(
            datetime.now() - timedelta(days=random.randint(1, 30))
        ).strftime('%Y-%m-%d'),
        roast_level=random.choice(['Light', 'Medium', 'Dark']),
        flavor_notes=random.sample(
            ['Floral', 'Citrus', 'Chocolate', 'Spice', 'Berry', 'Nutty'], 2
        ),
        submitted_by=random.choice(participant_ids),
    )
    coffees.append(coffee)
    coffee_ids.append(coffee_id)

    # Save coffee data
    coffee_file = os.path.join(COFFEES_DIR, f"{coffee_id}.yaml")
    with open(coffee_file, 'w') as f:
        yaml.safe_dump(coffee.model_dump(), f)

# Generate 3 sessions
session_dates = [
    (datetime.now() - timedelta(days=20)).strftime('%Y-%m-%d'),
    (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d'),
    datetime.now().strftime('%Y-%m-%d'),
]

for session_date in session_dates:
    session_dir = os.path.join(SESSIONS_DIR, session_date)
    ratings_dir = os.path.join(session_dir, 'ratings')
    rankings_dir = os.path.join(session_dir, 'rankings')
    os.makedirs(ratings_dir, exist_ok=True)
    os.makedirs(rankings_dir, exist_ok=True)

    # Sample 5 participants
    session_participants = random.sample(participants, 5)

    for participant in session_participants:
        # Generate ratings
        ratings = []
        for coffee in coffees:
            rating = Rating(
                coffee_id=coffee.coffee_id,
                sweetness=random.randint(1, 10),
                acidity=random.randint(1, 10),
                bitterness=random.randint(1, 10),
                body=random.randint(1, 10),
                aroma=random.randint(1, 10),
                flavor=random.randint(1, 10),
                aftertaste=random.randint(1, 10),
            )
            ratings.append(rating)

        participant_rating = ParticipantRating(
            participant_id=participant.participant_id,
            session_date=session_date,
            ratings=ratings,
        )

        # Save participant ratings
        ratings_file = os.path.join(
            ratings_dir, f"{participant.participant_id}.yaml"
        )
        with open(ratings_file, 'w') as f:
            yaml.safe_dump(participant_rating.model_dump(), f)

        # Generate rankings
        coffee_rankings = random.sample(coffee_ids, len(coffee_ids))
        rankings = []
        for rank, coffee_id in enumerate(coffee_rankings, start=1):
            ranking = Ranking(rank=rank, coffee_id=coffee_id)
            rankings.append(ranking)

        participant_ranking = ParticipantRanking(
            participant_id=participant.participant_id,
            session_date=session_date,
            rankings=rankings,
        )

        # Save participant rankings
        rankings_file = os.path.join(
            rankings_dir, f"{participant.participant_id}.yaml"
        )
        with open(rankings_file, 'w') as f:
            yaml.safe_dump(participant_ranking.model_dump(), f)

print('Dummy data generation complete.')
