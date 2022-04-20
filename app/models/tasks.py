from app.configs.database import db
from sqlalchemy import Column, Integer, String, Text, ForeignKey


class TasksModel(db.Model):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    duration = Column(Integer)
    importance = Column(Integer)
    urgency = Column(Integer)
    eisenhower = Column(Integer, ForeignKey("estados.id"), nullable=False)
