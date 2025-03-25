import os
from apis.base import api_router
from core.config import settings
from db.base import Base
from db.session import engine,SessionLocal
from fastapi import FastAPI, APIRouter, status,HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse
router = APIRouter()

def create_tables():
    Base.metadata.create_all(bind=engine)

# def run_migrations():
#     """Run Alembic migrations."""
#     alembic_config = os.path.join(os.path.dirname(__file__), "alembic.ini")
#     subprocess.run(["alembic", "-c", alembic_config, "upgrade", "head"], check=True)
class LoginRequest(BaseModel):
    username: str
    password: str
def include_router(app):
    app.include_router(api_router)


def configure_staticfiles(app):
    app.mount("/static", StaticFiles(directory="static"), name="static")
 

@router.get("/{page_name}")
def serve_html_page(page_name:str):
    print(page_name,"===========================")
    file_path = f"{page_name}.html"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    
    return {
        "data":[],
        "message": "Page not found",
        "status_code": status.HTTP_404_NOT_FOUND
    }

@router.post("/login")
async def login(request: LoginRequest):
    # Here you can add logic to verify the username and password (e.g., check a database)
    if request.username == "admin" and request.password == "password":  # Replace with actual logic
        return JSONResponse(content={"message": "Login successful", "status_code": status.HTTP_200_OK})
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

def start_application(): 
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    create_tables()
    include_router(app)
    configure_staticfiles(app)
    return app

origins = ['*']

app = start_application()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.on_event("startup")
def startup_event():
    # Initialize roles on startup
    
    try:
        db = SessionLocal()
    finally:
        db.close()