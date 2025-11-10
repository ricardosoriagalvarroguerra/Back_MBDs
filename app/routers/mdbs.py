from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from ..db.session import SessionLocal
from ..crud.mdbs import get_all_mdbs
from ..schemas.mdbs import Mdb as MdbSchema

router = APIRouter(prefix="/mdbs", tags=["mdbs"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[MdbSchema])
def list_mdbs(response: Response, db: Session = Depends(get_db)):
    response.headers["Cache-Control"] = "public, max-age=300"
    return get_all_mdbs(db)
