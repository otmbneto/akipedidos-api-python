from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from routers import auth,items,categories,reports
from pathlib import Path

# -----------------------------
# FastAPI Application
# -----------------------------

app = FastAPI(
    title="AkiPedidos Web API",
    description="FastAPI wrapper around the internal AkiPedidos scraping client.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(items.router)
app.include_router(categories.router)
app.include_router(reports.router)


BASE_DIR = Path(__file__).resolve().parent

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def root():
    html_path = BASE_DIR / "static" / "index.html"
    return html_path.read_text(encoding="utf-8")

@app.head("/", include_in_schema=False)
def root_head():
    return