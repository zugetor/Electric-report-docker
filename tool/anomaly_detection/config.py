import os

class Config(object):
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'db') #MySQL Host
    MYSQL_USER = os.getenv('MYSQL_USER', 'myuser') #MySQL username
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'verysecure') #MySQL password
    MYSQL_DB = os.getenv('MYSQL_DB', 'electric_mon') #MySQL DB name
    
    MONGODB_URL = os.getenv('MONGODB_URL', 'mongodb://root:password@mongo:27017/?authSource=admin') #MongoDB Connection String
    MONGODB_CONFIG_COLLECTION = os.getenv('MONGODB_COLLECTION', 'web_config')
    MONGODB_DATA_COLLECTION = os.getenv('MONGODB_COLLECTION', 'iot_data')