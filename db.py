# Simple SQLite helpers
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, DateTime, MetaData
from datetime import datetime

engine = create_engine("sqlite:///queuesense.db", echo=False)
meta = MetaData()

checkins = Table(
    "checkins", meta,
    Column("id", Integer, primary_key=True),
    Column("place_id", String),
    Column("wait_minutes", Integer),
    Column("timestamp", DateTime, default=datetime.utcnow),
)

meta.create_all(engine)
