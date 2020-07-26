class Config(object):
    DEBUG = False #Disable Debug
    MYSQL_HOST = 'db' #MySQL Host
    MYSQL_USER = 'myuser' #MySQL username
    MYSQL_PASSWORD = 'verysecure' #MySQL password
    MYSQL_DB = 'electric_mon' #MySQL DB name
    INFLUX_HOST = 'influxdb' #INFLUX Host
    INFLUX_USER = 'telegraf' #influxdb username
    INFLUX_PASSWORD = 'secretpassword' #influxdb password
    INFLUX_DB = 'electric_data' #INFLUX DB name
    SECRET_KEY = "mysecretkey" #your secret key
    SESSION_COOKIE_HTTPONLY = True #Cookie can access from HTTP Only
    REMEMBER_COOKIE_HTTPONLY = True #Cookie can access from HTTP Only
    ALLOW_REGISTER = True #Allow user to register
    ENABLE_DEV = True #Enable Development Config
    LOGIN_ONLY = True #Enable Login to all page and API
    TIME_ZONE = "Asia/Bangkok" #Time zone for check room schedule

class ProductionConfig(Config):
    DEBUG = False #Disable Debug
    SECRET_KEY = "Your Key" #your secret key for production
    RECAPTCHA_PUBLIC_KEY = "" #Recaptcha V2 public key from https://www.google.com/recaptcha
    RECAPTCHA_PRIVATE_KEY = "" #Recaptcha V2 private key from https://www.google.com/recaptcha
    RULE_UPDATE = 5 #Rule update every N minutes
    SCHEDULE_UPDATE = 60 #Schedule update every N minutes
    SENSOR_UPDATE = 60 #Check for new sensor every N minutes
    
class DevelopmentConfig(Config):
    DEBUG = True #Enable Debug
    RECAPTCHA_PUBLIC_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI" #Recaptcha public key for test only
    RECAPTCHA_PRIVATE_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe" #Recaptcha public key for test only
    RULE_UPDATE = 1 #Rule update every N minutes
    SCHEDULE_UPDATE = 1 #Schedule update every N minutes
    SENSOR_UPDATE = 1 #Check for new sensor every N minutes