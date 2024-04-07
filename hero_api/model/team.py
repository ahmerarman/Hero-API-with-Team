# This file shows circular import error, due to Hero model.
# I have tried all three methods to resolve the error.
# The only method works is to combine Team model and Hero model in one file.
# For this I have created database.py

"""from __future__ import annotations
from typing import Optional

from sqlmodel import Field, SQLModel, Relationship
#from sqlalchemy.orm import Mapped
from .hero import Hero

class TeamBase(SQLModel):
    name: str = Field(index=True)
    headquarters: str

class Team(TeamBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
#    heroes: list["Hero"] = Relationship(back_populates="team") # type: ignore
    heroes: list["Hero"] = Relationship(back_populates="team") # type: ignore"""