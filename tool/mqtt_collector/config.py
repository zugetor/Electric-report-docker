class Config(object):
    AMQP_HOST = 'rabbitmq' #  RabbitMQ  host
    AMQP_PORT = 5672 # RabbitMQ Port
    AMQP_USER = 'user' # RabbitMQ username
    AMQP_PASSWORD = 'password' # RabbitMQ password
    AMQP_VHOST = '/' # RabbitMQ VHOST
    AMQP_TOPIC = 'iot_data' # RabbitMQ topic
    MONGODB_URL = 'mongodb://root:password@mongo:27017/?authSource=admin' #MongoDB Connection String
    MONGODB_COLLECTION = 'iot_data'