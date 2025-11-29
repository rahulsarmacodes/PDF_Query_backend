from fastapi import FastAPI, status, Depends, HTTPException
from app.models import model
from app.db.database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes
from app.auth import auth
from app.auth.auth import get_current_user

app = FastAPI()
app.include_router(routes.router)
app.include_router(auth.router)


#cors setup
origins = [
    "http://localhost:5173",
    "https://pdf-query-frontend-kohl.vercel.app",
    "https://pdf-query-frontend-6zi6zzmm0-rahul-sarmas-projects.vercel.app",
    "https://pdf-query-frontend-git-main-rahul-sarmas-projects.vercel.app/"
    "https://*.vercel.app"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origin_regex=r"https://.*\.vercel\.app",
)



model.Base.metadata.create_all(bind=engine)
def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@app.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code =401, detail='Authentication Failed')
    return {"User": user}