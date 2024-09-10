from fastapi import FastAPI
from .routes import router as playlist_router
app = FastAPI()

app.include_router(playlist_router)
