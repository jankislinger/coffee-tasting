from typing import List, Optional

from pydantic import BaseModel, field_validator


class CoffeeBean(BaseModel):
    coffee_id: str
    name: str
    origin: str
    roaster: str
    roast_date: str  # You can use datetime.date if needed
    roast_level: str
    flavor_notes: List[str]
    submitted_by: str


class Participant(BaseModel):
    participant_id: str
    name: Optional[str]
    email: Optional[str]
    preferences: Optional[List[str]]


class Rating(BaseModel):
    coffee_id: str
    sweetness: int
    acidity: int
    bitterness: int
    body: int
    aroma: int
    flavor: int
    aftertaste: int

    @field_validator("*", mode="before")
    def check_rating(cls, v, field):
        if field.name in (
            "sweetness",
            "acidity",
            "bitterness",
            "body",
            "aroma",
            "flavor",
            "aftertaste",
        ):
            if not isinstance(v, int) or not 0 <= v <= 10:
                raise ValueError(f"{field.name} must be an integer between 0 and 10")
        return v


class ParticipantRating(BaseModel):
    participant_id: str
    session_date: str
    ratings: List[Rating]


class Ranking(BaseModel):
    rank: int
    coffee_id: str


class ParticipantRanking(BaseModel):
    participant_id: str
    session_date: str
    rankings: List[Ranking]
