from app import create_app
from app.extensions import db
from flask_migrate import Migrate
from flask.cli import FlaskGroup

app = create_app()
migrate = Migrate(app, db)

cli = FlaskGroup(create_app=create_app)

if __name__ == "__main__":
    cli()
