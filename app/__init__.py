from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
import os


db = SQLAlchemy()
migrate = Migrate()

def create_app():

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://postgres:postgres@localhost:5432/taskmanager'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.tasks import tasks_blp
    from app.routes.categories import categories_blp
    app.register_blueprint(tasks_blp)
    app.register_blueprint(categories_blp)

    return app