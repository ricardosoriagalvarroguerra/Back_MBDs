from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from ..db.session import SessionLocal
from ..crud.maturity import get_maturity_rows
from ..schemas.maturity import Maturity as MaturitySchema

router = APIRouter(prefix="/maturity", tags=["maturity"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[MaturitySchema])
def list_maturity_rows(
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    db: Session = Depends(get_db),
):
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date must be before or equal to end_date",
        )
    return get_maturity_rows(db, start_date=start_date, end_date=end_date)
