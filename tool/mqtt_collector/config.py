import os

class Config(object):
    AMQP_HOST = os.getenv('AMQP_HOST', 'rabbitmq') #  RabbitMQ  host
    AMQP_PORT = os.getenv('AMQP_PORT', '5672') # RabbitMQ Port
    AMQP_USER = os.getenv('AMQP_USER', 'users') # RabbitMQ username
    AMQP_PASSWORD = os.getenv('AMQP_PASSWORD', 'password') # RabbitMQ password
    AMQP_VHOST = os.getenv('AMQP_VHOST', '/') # RabbitMQ VHOST
    AMQP_TOPIC = os.getenv('AMQP_TOPIC', 'mqtt_data') # RabbitMQ topic

    MYSQL_HOST = os.getenv('MYSQL_HOST', 'db') #MySQL Host
    MYSQL_USER = os.getenv('MYSQL_USER', 'myuser') #MySQL username
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'verysecure') #MySQL password
    MYSQL_DB = os.getenv('MYSQL_DB', 'electric_mon') #MySQL DB name
    MONGODB_URL = os.getenv('MONGODB_URL', 'mongodb://root:password@mongo:27017/?authSource=admin') #MongoDB Connection String
    MONGODB_COLLECTION = os.getenv('MONGODB_COLLECTION', 'iot_data')