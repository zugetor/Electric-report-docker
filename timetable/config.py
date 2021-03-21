class Config(object):
    DEBUG = False #Disable Debug
    MYSQL_HOST = 'db' #MySQL Host
    MYSQL_USER = 'myuser' #MySQL username
    MYSQL_PASSWORD = 'verysecure' #MySQL password
    MYSQL_DB = 'electric_mon' #MySQL DB name
    ENABLE_DEV = True #Enable Development Config
    TIME_ZONE = "Asia/Bangkok" #Time zone for check room schedule
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
    RULE_UPDATE = 5 #Rule update every N minutes
    SCHEDULE_UPDATE = 60 #Schedule update every N minutes
    SENSOR_UPDATE = 60 #Check for new sensor every N minutes
    
class DevelopmentConfig(Config):
    DEBUG = True #Enable Debug
    RULE_UPDATE = 0.1 #Rule update every N minutes
    SCHEDULE_UPDATE = 0.1 #Schedule update every N minutes
    SENSOR_UPDATE = 0.1 #Check for new sensor every N minutes