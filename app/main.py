from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.core.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def serve_frontend():
    return FileResponse("app/static/index.html")
