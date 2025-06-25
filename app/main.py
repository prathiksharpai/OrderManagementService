from fastapi import FastAPI
from . import models, database
from app.routes import router

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Order Management Service")

app.include_router(router)

