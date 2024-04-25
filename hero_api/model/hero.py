# This file shows circular import error, due to Team model.
# I have tried all three methods to resolve the error.
# The only method works is to combine Team model and Hero model in one file.
# For this I have created database.py

"""from __future__ import annotations
from typing import Optional

from sqlmodel import Field, SQLModel, Relationship
#from sqlalchemy.orm import Mapped
#from hero_api.model.team import Team

class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None)
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")

class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    team: Optional["Team"] = Relationship(back_populates="heroes") # type: ignore"""

