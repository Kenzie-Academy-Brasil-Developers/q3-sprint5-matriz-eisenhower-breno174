from app.configs.database import db
from sqlalchemy import Column, Integer, String, Text


class CategoriesModel(db.Model):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
