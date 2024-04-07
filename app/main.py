from fastapi import FastAPI, HTTPException
from app.db import create_db_tables
from contextlib import asynccontextmanager
from hero_api.routes.hero import hero_router
from hero_api.routes.team import team_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print("Creating tables....")
        create_db_tables()
    except:
        raise HTTPException(status_code=400, detail="Bad request.")
    yield

app = FastAPI(lifespan=lifespan,
                title="UIT Fast API",
                version="0.0.1")
app.include_router(hero_router)
app.include_router(team_router)

@app.get("/")
async def hello_world():
    return {"message":"Hello! World. Hero API is running."}
