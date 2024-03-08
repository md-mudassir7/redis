from python.routers import tasks
from fastapi import FastAPI

def main_app():
    app = FastAPI()

    app.include_router(tasks.router)

    return app