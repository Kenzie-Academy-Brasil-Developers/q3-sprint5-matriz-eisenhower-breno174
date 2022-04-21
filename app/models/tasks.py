from app.models.task_categores import task_categories
from app.configs.database import db
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship


class TasksModel(db.Model):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    duration = Column(Integer)
    importance = Column(Integer)
    urgency = Column(Integer)
    eisenhower_id = Column(Integer, ForeignKey("eisenhower.id"), nullable=False)

    categories = relationship("CategoriesModel", secondary=task_categories, backref="tasks")
