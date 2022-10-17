from flask import Flask
from flask_injector import FlaskInjector

from dependencies import configure

from adapters.http.controllers.users_controller import app_users
from adapters.http.controllers.account_controller import app_account

app = Flask(__name__)

app.register_blueprint(app_users)
app.register_blueprint(app_account)

FlaskInjector(app=app, modules=[configure])
