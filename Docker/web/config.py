class Config(object):
    DEBUG = False
    TESTING = False
    MYSQL_HOST = 'db'
    MYSQL_USER = 'myuser' #MySQL username
    MYSQL_PASSWORD = 'verysecure' #MySQL password
    MYSQL_DB = 'electric_mon'
    INFLUX_HOST = 'influxdb'
    INFLUX_USER = 'telegraf' #influxdb username
    INFLUX_PASSWORD = 'secretpassword' #influxdb password
    INFLUX_DB = 'electric_data'
    SECRET_KEY = "mysecretkey" #your secret key
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "Your Key"
    
class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True