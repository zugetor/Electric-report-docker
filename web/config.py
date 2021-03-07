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
    INF_TABLE = ["ct","dm","pir"] #Name of table in InfluxDB
    Nofify_Template = "Rule: {rname}\nDate: {date}\nDay: {dow}\nTime: {time}\nBuilding: {building}\nfloor: {floor}\nRoom: {room}\nStatus: {status}\nLight: {light}\nPlug: {plug}\nAir: {air}\nPir: {pir}\n"
    #{rname} = Rule Name
    #{date} = Current Date at notify time
    #{dow} = Current Day name at notify time
    #{time} = Current Hour in 24H. at notify time
    #{building} = Building name
    #{floor} = Floor name
    #{room} = Room name
    #{status} = Room status
    #{light} = Current amp light using at notify time
    #{plug} = Current amp plug using at notify time
    #{air} = Current amp air using at notify time
    #{pir} = Current motion using at notify time

class ProductionConfig(Config):
    DEBUG = False #Disable Debug
    RECAPTCHA_PUBLIC_KEY = "" #Recaptcha V2 public key from https://www.google.com/recaptcha
    RECAPTCHA_PRIVATE_KEY = "" #Recaptcha V2 private key from https://www.google.com/recaptcha
    RULE_UPDATE = 5 #Rule update every N minutes
    SCHEDULE_UPDATE = 60 #Schedule update every N minutes
    SENSOR_UPDATE = 60 #Check for new sensor every N minutes
    
class DevelopmentConfig(Config):
    DEBUG = True #Enable Debug
    RECAPTCHA_PUBLIC_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI" #Recaptcha public key for test only
    RECAPTCHA_PRIVATE_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe" #Recaptcha public key for test only
    RULE_UPDATE = 0.1 #Rule update every N minutes
    SCHEDULE_UPDATE = 0.1 #Schedule update every N minutes
    SENSOR_UPDATE = 0.1 #Check for new sensor every N minutes