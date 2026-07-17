from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from web.api import api_router

app = FastAPI()

app.include_router(api_router, prefix="/api")


@app.get("/")
def index():
    return FileResponse("dist/index.html")


app.mount("/", StaticFiles(directory="dist"), name="dist")
