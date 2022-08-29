from fastapi import FastAPI
from database import engine
import router1
import models
import home
import admin
import router2
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(home.home)
app.include_router(router1.router)
app.include_router(router2.order)
app.include_router(admin.Admin)

