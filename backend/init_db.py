from app import create_app, db
from app.models import init_db

app = create_app()
with app.app_context():
    init_db() 