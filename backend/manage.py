from flask.cli import FlaskGroup
from app import create_app
from alembic import command
from alembic.config import Config

app = create_app()
cli = FlaskGroup(app)

@cli.command("db_migrate")
def db_migrate():
    """Generate a new migration"""
    alembic_cfg = Config("alembic.ini")
    command.revision(alembic_cfg, autogenerate=True)

@cli.command("db_upgrade")
def db_upgrade():
    """Apply all migrations"""
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

if __name__ == '__main__':
    cli() 