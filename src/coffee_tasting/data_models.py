from typing import List

from pydantic import BaseModel, field_validator


class Coffee(BaseModel):
    coffee_id: str
    url: str
    image_url: str
    name: str
    roaster: str
    origin: str
    process_method: str
    roast_level: str
    flavor_notes: List[str]


class CoffeeBatch(BaseModel):
    coffee_id: str
    session_date: str
    submitted_by: str
    roast_date: str
    crop_date: str
    weight: int
    price: float


class Rating(BaseModel):
    overall: int
    acidity: int
    aftertaste: int
    aroma: int
    bitterness: int
    body: int
    flavor: int
    sweetness: int

    @field_validator("*", mode="before")
    def check_rating(cls, v, field):
        if not isinstance(v, int) or not 0 <= v <= 10:
            raise ValueError(f"{field.name} must be an integer between 0 and 10")
        return v


class Ranking(BaseModel):
    rank: int
    coffee_id: str
    rating: Rating
    notes: str


class ParticipantRanking(BaseModel):
    participant_id: str
    session_date: str
    rankings: List[Ranking]
