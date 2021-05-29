import pika, sys, os, json, pymongo
from time import time
from extensions import getConfig

cfg = getConfig()
client = pymongo.MongoClient(cfg.MONGODB_URL)

def callback(ch, method, properties, body):
	try:
		body = json.loads(body)
		topicRaw = method.routing_key
		topic = method.routing_key.split(".")
		sensorType = ""
		deviceType = ""
		if(len(topic) == 7):
			sensorType = topic[len(topic) - 2]
			deviceType = topic[len(topic) - 1]
			collectionName = sensorType + "_" + deviceType
		else:
			sensorType = topic[len(topic) - 1]
			collectionName = sensorType

		print("-" * 50)
		print("Received: %r" % body)
		print("Routing key: %r" % topicRaw)
		print("Collection name: %r" % collectionName)

		schema = {}
		if(isinstance(body, dict)):
			for key in body.keys():
				_class = class2Str(body[key])
				if(_class != None):
					schema[key] = _class

		db = client[cfg.MONGODB_COLLECTION]
		_type = {"sensor_type": sensorType, "device_type": deviceType, "schema": schema}
		db["iot_type"].update(_type, _type, upsert=True)

		doc = {}
		doc["topic"] = topicRaw.replace(".","/")
		doc["created_at"] = int(time())
		doc["message"] = body
		db[collectionName].insert_one(doc)
		ch.basic_ack(delivery_tag = method.delivery_tag)
	except ValueError:
		print("[ERROR] ValueError: ", body)
		ch.basic_ack(delivery_tag = method.delivery_tag)
	except Exception as e:
		print("[ERROR] Error: ", e)
		ch.basic_nack(delivery_tag = method.delivery_tag)

def class2Str(val):
	if(isinstance(val, str)):
		return "string"
	if(isinstance(val, int)):
		return "int"
	if(isinstance(val, bool)):
		return "bool"
	return None

if __name__ == '__main__':
	try:
		credentials = pika.PlainCredentials(cfg.AMQP_USER, cfg.AMQP_PASSWORD)
		parameters = pika.ConnectionParameters(cfg.AMQP_HOST, cfg.AMQP_PORT, cfg.AMQP_VHOST, credentials)
		connection = pika.BlockingConnection(parameters)
		channel = connection.channel()

		channel.queue_declare(queue=cfg.AMQP_TOPIC, durable=True)
		channel.basic_consume(queue=cfg.AMQP_TOPIC, on_message_callback=callback)

		print('Waiting for messages. To exit press CTRL+C')
		channel.start_consuming()
	except KeyboardInterrupt:
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)