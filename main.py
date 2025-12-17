from fastapi import FastAPI
from akipedidos.client import AkiPedidosClient
from routers import auth,items,categories

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
