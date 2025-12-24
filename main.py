from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from routers import auth,items,categories,reports

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

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def root():
    return """
    <html>
        <head>
            <title>Pedlog API</title>
        </head>
        <body>
            <h1>Pedlog API</h1>
            <p>Welcome to the main page of the Web API</p>

            <ul>
                <li><a href="/docs">Swagger UI</a></li>
                <li><a href="/redoc">ReDoc</a></li>
            </ul>
        </body>
    </html>
    """