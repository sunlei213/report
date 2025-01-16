from app import db

def init_db():
    db.create_all()

def drop_db():
    db.drop_all() 