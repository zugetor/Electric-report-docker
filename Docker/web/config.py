class Config(object):
    DEBUG = False
    TESTING = False
    MYSQL_HOST = 'db'
    MYSQL_USER = 'myuser'
    MYSQL_PASSWORD = 'verysecure'
    MYSQL_DB = 'electric_mon'
    INFLUX_HOST = 'influxdb'
    INFLUX_USER = 'telegraf'
    INFLUX_PASSWORD = 'secretpassword'
    INFLUX_DB = 'electric_data'
    SECRET_KEY = "mysecretkey"

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "Your Key"
    
class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True