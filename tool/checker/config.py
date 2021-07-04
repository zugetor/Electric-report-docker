import os

class Config(object):
    DEBUG = (os.getenv("DEBUG", 'False').lower() in ('true', '1', 't')) #Disable Debug
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'db') #MySQL Host
    MYSQL_USER = os.getenv('MYSQL_USER', 'myuser') #MySQL username
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'verysecure') #MySQL password
    MYSQL_DB = os.getenv('MYSQL_DB', 'electric_mon') #MySQL DB name
    MONGODB_URL = os.getenv('MONGODB_URL', 'mongodb://root:password@mongo:27017/?authSource=admin') #MongoDB Connection String
    MONGODB_COLLECTION = os.getenv('MONGODB_COLLECTION', 'iot_data')
    TIME_ZONE = os.getenv('TIME_ZONE', 'Asia/Bangkok') #Time zone for check room schedule
    SHOW_SENSOR_VALUE = (os.getenv("SHOW_SENSOR_VALUE", 'False').lower() in ('true', '1', 't')) # show sensor value in notify message(Message might be overflow)
    Nofify_Template = "\nRule: {rname}\nDate: {date}\nDay: {dow}\nTime: {time}\nBuilding: {building}\nFloor: {floor}\nRoom: {room}\nStatus: {status}"
    #{rname} = Rule Name
    #{date} = Current Date at notify time
    #{dow} = Current Day name at notify time
    #{time} = Current Hour in 24H. at notify time
    #{building} = Building name
    #{floor} = Floor name
    #{room} = Room name
    #{status} = Room status