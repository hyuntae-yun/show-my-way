from flask import Flask
from jogging.routes import user_routes, map_routes
from jogging.models import db, migrate

DATABASE_URI='postgres://mqeribwf:r258bjB4hxpUhLmeucWvU2T4HV1_OKzQ@john.db.elephantsql.com:5432/mqeribwf'

def create_app():
    app=Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate.init_app(app, db)
    
    app.register_blueprint(user_routes.user_routes)
    app.register_blueprint(map_routes.map_routes, url_prefix='/')
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)