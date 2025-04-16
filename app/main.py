from fastapi import FastAPI

from app.auth.controller import router as auth_router
from app.records.controller import router as records_router
from app.users.controller import router as users_router

app = FastAPI()

app.include_router(users_router)
app.include_router(records_router)
app.include_router(auth_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
