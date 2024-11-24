class Config():
    DEBUG = False
    SQL_ALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite3"
    DEBUG = True
    SECURITY_REGISTRABLE = True
    SECURITY_JOIN_USER_ROLES = True
    SECURITY_TRACKABLE = True
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = 'householdservicesapplicationasecretstring'
    SECRET_KEY = 'asecretkey'
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authorization'
    
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_DEFAULT_TIMEOUT = 60 #caching for 1 min

    MAIL_SERVER = 'localhost'
    MAIL_PORT = 1025
    MAIL_DEFAULT_SENDER = 'no-reply@a.com'

    WTF_CSRF_ENABLED = False
    