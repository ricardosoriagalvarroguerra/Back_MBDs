from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models.mdbs import Mdb


def get_all_mdbs(db: Session) -> list[Mdb]:
    stmt = select(Mdb).order_by(Mdb.mdb_id)
    return db.execute(stmt).scalars().all()
