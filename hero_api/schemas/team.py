# This file shows circular import error, due to hero.py.
# I have tried all three methods to resolve the error.
# The only method works is to combine team.py model and hero.py model in one file.
# For this, I have created schemas.py

"""from __future__ import annotations
from typing import Optional
from sqlmodel import SQLModel
from hero_api.model.database import TeamBase
#import HeroRead # type: ignore
from hero_api.schemas.hero import HeroRead # type : ignore
#from hero_api.model.team import TeamBase

#class TeamBase(SQLModel):
#    name: str
#    headquarters: str

class TeamCreate(TeamBase):
    pass

class TeamRead(TeamBase):
    id: int

class TeamUpdate(SQLModel):
    name: str | None = None
    headquarters: str | None = None

class TeamUpdateComplete(TeamUpdate):
    pass

class TeamReadWithHeroes(TeamRead):
    heroes: Optional[list[HeroRead]] = [] # type : ignore"""
