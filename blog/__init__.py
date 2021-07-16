from flask import Flask
from .database import create_database
from .login_manager import manage_login


def create_app():
	app = Flask(__name__, template_folder='template')
	app.config['SECRET_KEY'] = 'This is a secret key'
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

	from .views import views
	from .auth import auth
	from .models import Post, User, Contact

	create_database(app)
	manage_login(app)

	app.register_blueprint(views, url_prefix='/')
	app.register_blueprint(auth, url_prefix='/')

	return app
