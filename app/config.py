import os

base_dir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = 'kenedi123',
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(base_dir,'db.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

class Config_Production(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = False

class Config_Development(Config):
    SECRET_KEY = 'kenedi123'
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    PRAETORIAN_HASH_SCHEME = 'pbkdf2_sha512'
    JWT_ALLOWED_ALGORITHMS = ['HS256']
    JWT_ALGORITHM = 'HS256'
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    JWT_ACCESS_LIFESPAN = {'hours':24}
    JWT_REFRESH_LIFESPAN = {'days': 30}
    USER_CLASS_VALIDATION_METHOD = 'is_valid'
    DEFAULT_RENDERERS = ['flask_api.renderers.JSONRenderer','flask_api.renderers.BrowsableAPIRenderer']
    DEFAULT_PARSERS = ['flask_api.parsers.JSONParser','flask_api.parsers.URLEncodedParser','flask_api.parsers.MultiPartParser']
    RESTPLUS_VALIDATE = True
    SWAGGER_UI_DOC_EXPANSION = 'list'
    SWAGGER_SUPPORTED_SUBMIT_METHODS = ['get','post','delete','put']
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'kenedynpsyh@gmail.com'
    MAIL_PASSWORD = 'Kenedi@123'

