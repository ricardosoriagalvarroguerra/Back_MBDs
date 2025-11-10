from pydantic import BaseModel


class Mdb(BaseModel):
    mdb_id: int
    mdb_code: str | None = None
    mdb_name: str

    class Config:
        from_attributes = True
