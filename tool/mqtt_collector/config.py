class Config(object):
    AMQP_HOST = 'rabbitmq' #  RabbitMQ  host
    AMQP_PORT = 5672 # RabbitMQ Port
    AMQP_USER = 'user' # RabbitMQ username
    AMQP_PASSWORD = 'password' # RabbitMQ password
    AMQP_VHOST = '/' # RabbitMQ VHOST
    AMQP_TOPIC = 'iot_data' # RabbitMQ topic
    MYSQL_HOST = 'db' #MySQL Host
    MYSQL_USER = 'myuser' #MySQL username
    MYSQL_PASSWORD = 'verysecure' #MySQL password
    MYSQL_DB = 'electric_mon' #MySQL DB name
    MONGODB_URL = 'mongodb://root:password@mongo:27017/?authSource=admin' #MongoDB Connection String
    MONGODB_COLLECTION = 'iot_data'