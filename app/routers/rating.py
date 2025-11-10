from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from ..db.session import SessionLocal
from ..crud.rating import get_rating_rows
from ..schemas.rating import Rating as RatingSchema

router = APIRouter(prefix="/rating", tags=["rating"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[RatingSchema])
def list_rating_rows(
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    db: Session = Depends(get_db),
):
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date must be before or equal to end_date",
        )
    return get_rating_rows(db, start_date=start_date, end_date=end_date)
