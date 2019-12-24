from flask import Flask
from app.config import Config_Development,Config_Production
from app.serializer.extension import config_extension

class Servers:
    def create_app(config_prod=Config_Production,config_dev=Config_Development):
        app = Flask('Kenedi Novriansyah')
        if app.config['ENV'] == 'production':
            app.config.from_object(config_prod)
        else:
            app.config.from_object(config_dev)
        config_extension(app)
        return app
