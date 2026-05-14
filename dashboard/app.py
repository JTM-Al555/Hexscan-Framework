from pathlib import Path

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(
    directory=str(
        BASE_DIR / "templates"
    )
)

app = FastAPI(
    title="AI Recon Dashboard",
    version="1.0.0"
)

# OPTIONAL STATIC FILES
static_dir = BASE_DIR / "static"

if static_dir.exists():

    app.mount(
        "/static",
        StaticFiles(
            directory=str(static_dir)
        ),
        name="static"
    )


@app.get(
    "/",
    response_class=HTMLResponse
)
async def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": (
                "AI Recon Dashboard"
            )
        }
    )


@app.get("/health")
async def health():

    return {
        "status": "online"
    }