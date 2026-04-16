from fastapi import FastAPI
from app.database import Base,engine
from app import models
from app.routers import expense
from app.routers import user
from app.routers import auth

models.Base.metadata.create_all(bind=engine)

app=FastAPI()


app.include_router(expense.router)
app.include_router(user.router)
app.include_router(auth.router)


