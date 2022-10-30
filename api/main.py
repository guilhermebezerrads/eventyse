from flask import Flask

from adapters.rest.controllers.accounts_controller import create_accounts_blueprint
from adapters.rest.controllers.users_controller import create_users_blueprint
from adapters.rest.controllers.follows_controller import create_follows_blueprint
from adapters.rest.controllers.roadmaps_controller import create_roadmaps_blueprint
from adapters.rest.controllers.rate_controller import create_rates_blueprint
from adapters.rest.controllers.comments_controller import create_comment_blueprint
from adapters.rest.controllers.exceptions_controller import create_exceptions_blueprint

from configuration import configure_api, configure_inject

def create_api() -> Flask:
    api = Flask(__name__)

    configure_api(api)
    configure_inject(api)

    api.register_blueprint(create_exceptions_blueprint())
    
    api.register_blueprint(create_accounts_blueprint(), url_prefix='/api')
    api.register_blueprint(create_users_blueprint(), url_prefix='/api')
    api.register_blueprint(create_follows_blueprint(), url_prefix='/api')
    api.register_blueprint(create_roadmaps_blueprint(), url_prefix='/api')
    api.register_blueprint(create_rates_blueprint(), url_prefix='/api')
    api.register_blueprint(create_comment_blueprint(), url_prefix='/api')

    return api

api: Flask = create_api()
api.run()
