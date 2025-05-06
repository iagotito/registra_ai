import os

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.auth.controller import router as auth_router
from app.records.controller import router as records_router
from app.users.controller import router as users_router
from app.users.services import get_current_user

app_dir = os.path.dirname(os.path.abspath(__file__))
static_folder = os.path.abspath(os.path.join(app_dir, "../static"))
template_folder = os.path.abspath(os.path.join(app_dir, "../static/templates"))

app = FastAPI()

app.mount("/static", StaticFiles(directory=static_folder), name="static")
templates = Jinja2Templates(directory=template_folder)

app.include_router(users_router)
app.include_router(records_router)
app.include_router(auth_router)


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/login", response_class=HTMLResponse)
async def get_login(request: Request):
    response = templates.TemplateResponse(
        "login.html", {"request": request, "base_url": "http://localhost:8000"}
    )
    return response


@app.get("/api/authenticated", response_class=HTMLResponse)
async def get_authenticated(
    request: Request, user_data: dict = Depends(get_current_user)
):
    if not user_data:
        raise HTTPException(status_code=401, detail="Authentication required")
    response = templates.TemplateResponse(
        "authenticated.html", {"request": request, "user": user_data}
    )
    return response
