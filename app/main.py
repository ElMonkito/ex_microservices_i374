from fastapi import FastAPI
from app.database import Base, engine
from app.routers import commandes

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(commandes.router)
