from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager
from flask_cors import CORS

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()



def create_app(config_class=Config):  # Allow passing a config class
    app = Flask(__name__)
    CORS(app)  # Put CORS in the setup for flask app
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    login_manager = LoginManager(app)
    login_manager.login_view = "auth.signin"

    from app.models import Users

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    from app.auth import auth as auth_blueprint
    
    

    # app.register_blueprint(auth_blueprint, url_prefix="/auth")

    print("Registering blueprints...")
    try:
        from app.auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint, url_prefix="/auth")
        print("Blueprint registered successfully!")
    except Exception as e:
        print(f"Error during blueprint registration: {e}")

    return app
