from app.configs.database import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref


class EisenhowerModel(db.Model):
    __tablename__ = "eisenhower"

    id = Column(Integer, primary_key=True)
    type = Column(String(100))

    tasks = relationship("TasksModel", backref=backref("eisenhower", uselist=False), uselist=True)
