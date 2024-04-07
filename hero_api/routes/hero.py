from sqlmodel import Session, select
from app.db import get_session
from hero_api.model.database import Hero
from fastapi import APIRouter, HTTPException, Query, Depends
from hero_api.schemas.schemas import HeroCreate, HeroRead, HeroUpdate, HeroUpdateComplete, HeroReadWithTeam

hero_router = APIRouter(prefix="/heroes", tags=["Hero"])

@hero_router.post("/", response_model=HeroRead)
def create_hero(*, session: Session = Depends(get_session), hero: HeroCreate):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

@hero_router.get("/", response_model=list[HeroRead])
def read_heroes(*, session: Session = Depends(get_session), offset: int = 0, limit: int = Query(default=100, le=100)):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes

@hero_router.get("/{hero_id}", response_model=HeroReadWithTeam)
def read_hero(*, session: Session = Depends(get_session), hero_id: int):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Record not found.")
    return hero

@hero_router.patch("/{hero_id}", response_model=HeroRead)
def update_hero(*, session: Session = Depends(get_session), hero_id: int, hero: HeroUpdate):
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Record not found.")
    hero_data = hero.model_dump(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(db_hero, key, value)
    #db_hero.sqlmodel_update(hero_data)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

@hero_router.put("/{hero_id}", response_model=HeroRead)
async def change_heroes(*, session: Session = Depends(get_session), hero_id: int, hero: HeroUpdateComplete):
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Record not found.")
    try:
        hero_data = hero.model_dump(exclude_unset=False)
        for key, value in hero_data.items():
            setattr(db_hero, key, value)
        #db_hero.sqlmodel_update(hero_data)
        session.add(db_hero)
        session.commit()
        session.refresh(db_hero)
    except:
        raise HTTPException(status_code=422, detail="Invalid data.")
    return db_hero

@hero_router.delete("/{hero_id}", response_model=HeroRead)
async def delete_hero(*, session: Session = Depends(get_session), hero_id: int):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Record not found.")
    session.delete(hero)
    session.commit()
    return hero
