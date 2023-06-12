from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey
from uuid import uuid4

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String),
    Column("access_token", String)
)

recordings = Table(
    "recordings",
    metadata,
    Column("id", String, primary_key=True, default=lambda: str(uuid4())),
    Column("path", String),
    Column("user_id", Integer, ForeignKey("users.id")),
)

