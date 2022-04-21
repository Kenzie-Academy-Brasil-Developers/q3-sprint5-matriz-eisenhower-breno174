from app.configs.database import db
# from sqlalchemy import Table, Column, Integer, ForeignKey

task_categories = db.Table('task_categories',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'))
)
