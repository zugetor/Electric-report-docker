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
    ALLOW_REGISTER = True #Allow user to register
    ENABLE_DEV = True #Enable Development Config
    LOGIN_ONLY = True #Enable Login to all page and API

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "Your Key" #your secret key for production
    RECAPTCHA_PUBLIC_KEY = "" #Recaptcha public key
    RECAPTCHA_PRIVATE_KEY = "" #Recaptcha private  key
    RULE_UPDATE = 5 #Rule update every N minutes
    SCHEDULE_UPDATE = 60 #Schedule update every N minutes
    
class DevelopmentConfig(Config):
    DEBUG = True
    RECAPTCHA_PUBLIC_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI" #Recaptcha public key for test only
    RECAPTCHA_PRIVATE_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe" #Recaptcha public key for test only
    RULE_UPDATE = 1 #Rule update every N minutes
    SCHEDULE_UPDATE = 1 #Schedule update every N minutes

class TestingConfig(Config):
    TESTING = True