from fastapi import FastAPI
from routes.readings import router as readings_router
from routes.machines import router as machines_router

app = FastAPI()
app.include_router(readings_router)
app.include_router(machines_router)

