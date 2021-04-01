class Config(object):
    DEBUG = False #Disable Debug
    MYSQL_HOST = 'db' #MySQL Host
    MYSQL_USER = 'myuser' #MySQL username
    MYSQL_PASSWORD = 'verysecure' #MySQL password
    MYSQL_DB = 'electric_mon' #MySQL DB name
    MONGODB_URL = 'mongodb://root:password@mongo:27017/?authSource=admin' #MongoDB Connection String
    MONGODB_COLLECTION = 'iot_data'
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