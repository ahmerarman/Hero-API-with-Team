from typing import Optional
from sqlmodel import SQLModel
from hero_api.model.database import HeroBase, TeamBase

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
    team: Optional["TeamRead"] = None

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
    heroes: Optional[list[HeroRead]] = []

