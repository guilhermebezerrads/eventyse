from flask import Flask
from adapters.http.controllers.account_controller import create_account_blueprint
from adapters.http.controllers.users_controller import create_users_blueprint
from configuration import configure_api, configure_inject

def create_api() -> Flask:
    api = Flask(__name__)

    configure_api(api)
    configure_inject(api)

    api.register_blueprint(create_account_blueprint(), url_prefix='/api')
    api.register_blueprint(create_users_blueprint(), url_prefix='/api')

    return api

api: Flask = create_api()
api.run()
