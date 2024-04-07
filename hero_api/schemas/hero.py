# This file shows circular import error, due to team.py.
# I have tried all three methods to resolve the error.
# The only method works is to combine team.py model and hero.py model in one file.
# For this, I have created schemas.py

"""from __future__ import annotations
from typing import Optional
from sqlmodel import SQLModel
from hero_api.model.database import HeroBase
from hero_api.schemas.team import TeamRead
#from hero_api.model.hero import HeroBase

#class HeroBase(SQLModel):
#    name: str
#    secret_name: str
#    age: int | None = None
#    team_id: int | None = None

class HeroCreate(HeroBase):
    pass

class HeroRead(HeroBase):
    id: int

class HeroUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None
    team_id: int | None = None

class HeroUpdateComplete(HeroUpdate):
    pass

class HeroReadWithTeam(HeroRead):
    team: Optional["TeamRead"] = None # type : ignore"""
