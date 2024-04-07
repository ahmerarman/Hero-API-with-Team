from sqlmodel import Session, select
from app.db import get_session
from hero_api.model.database import Team
from fastapi import APIRouter, HTTPException, Query, Depends
from hero_api.schemas.schemas import TeamCreate, TeamRead, TeamUpdate, TeamUpdateComplete, TeamReadWithHeroes

team_router = APIRouter(prefix="/teams", tags=["Team"])

@team_router.post("/", response_model=TeamRead)
def create_team(*, session: Session = Depends(get_session), team: TeamCreate):
    db_team = Team.model_validate(team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team

@team_router.get("/", response_model=list[TeamRead])
def read_teams(*, session: Session = Depends(get_session), offset: int = 0, limit: int = Query(default=100, le=100)):
    teams = session.exec(select(Team).offset(offset).limit(limit)).all()
    return teams

@team_router.get("/{team_id}", response_model=TeamReadWithHeroes)
def read_team(*, session: Session = Depends(get_session), team_id: int):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Record not found.")
    return team

@team_router.patch("/{team_id}", response_model=TeamRead)
def update_team(*, session: Session = Depends(get_session), team_id: int, team: TeamUpdate):
    db_team = session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Record not found.")
    team_data = team.model_dump(exclude_unset=True)
    for key, value in team_data.items():
        setattr(db_team, key, value)
    #db_team.sqlmodel_update(team_data)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team

@team_router.put("/{team_id}", response_model=TeamRead)
async def change_teams(*, session: Session = Depends(get_session), team_id: int, team: TeamUpdateComplete):
    db_team = session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Record not found.")
    try:
        team_data = team.model_dump(exclude_unset=False)
        for key, value in team_data.items():
            setattr(db_team, key, value)
        #db_team.sqlmodel_update(team_data)
        session.add(db_team)
        session.commit()
        session.refresh(db_team)
    except:
        raise HTTPException(status_code=422, detail="Invalid data.")
    return db_team

@team_router.delete("/{team_id}", response_model=TeamRead)
async def delete_team(*, session: Session = Depends(get_session), team_id: int):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Record not found.")
    session.delete(team)
    session.commit()
    return team
