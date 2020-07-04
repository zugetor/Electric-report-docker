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
    ALLOW_REGISTER = False #Allow user to register

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "Your Key" #your secret key for production
    RECAPTCHA_PUBLIC_KEY = "" #Recaptcha public key
    RECAPTCHA_PRIVATE_KEY = "" #Recaptcha private  key
    
class DevelopmentConfig(Config):
    DEBUG = True
    RECAPTCHA_PUBLIC_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI" #Recaptcha public key for test only
    RECAPTCHA_PRIVATE_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe" #Recaptcha public key for test only

class TestingConfig(Config):
    TESTING = True