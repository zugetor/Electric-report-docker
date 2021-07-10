import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pyod.models.knn import KNN
from joblib import dump, load
import time, threading, datetime, io
from bson.objectid import ObjectId
from config import Config
from notify import linenotify
from db import MySQL, MongoDB

enable_anomaly = False
start = datetime.datetime.today()

def initMongo():
	mongo = MongoDB()
	mongo.init_cfg(Config)
	_client = mongo.get_client()
	return _client

def getConfig():
	res = {}
	with initMongo() as _client:
		_db = _client[Config.MONGODB_CONFIG_COLLECTION]
		_collection = _db["key_storage"]
		res["detections"] = _collection.find_one({"key":"detections"})["value"]
		res["training"] = int(_collection.find_one({"key":"training"})["value"])
		res["datasize"] = None
		datasize = int(_collection.find_one({"key":"datasize"})["value"])
		if(datasize > 0):
			res["datasize"] = datasize
		res["enable"] = False
		if(_collection.find_one({"key":"enable"})["value"].lower() in ["y", "yes", "t", "true","1"]):
			res["enable"] = True
	return res

def initMySQL():
	mysql = MySQL()
	mysql.init_cfg(Config)
	_con = mysql.get_connection()
	return _con

def getToken():
	with initMySQL() as _cur:
		_cur.execute("SELECT * FROM notify")
		return _cur.fetchall()

def newLog(message,token):
	with initMySQL() as _cur:
		_cur.execute("DELETE FROM logs WHERE create_time <	(CURRENT_TIMESTAMP - INTERVAL 3 MONTH)")
		_cur.execute("INSERT INTO `logs` (`lid`, `message`, `create_time`) VALUES (NULL, %s, CURRENT_TIMESTAMP)",(message,))
		_cur.execute("UPDATE `notify` SET `nlast_time` = CURRENT_TIMESTAMP WHERE `notify`.`ntoken` = %s",(token,))

def preprocessing(query={},limit=None):
	config = getConfig()
	df = pd.DataFrame()
	with initMongo() as _client:
		_db = _client[Config.MONGODB_DATA_COLLECTION]
		for topic in config["detections"]:
			topic = topic.rsplit('_', 1)
			collectionName = topic[0]
			keyName = topic[1]
			print("Processing: ", topic)
			if(limit != None and int(limit) > 0):
				data = _db[collectionName].find(query, { "message": 1, "_id": 0 }, limit=limit, batch_size=500).sort('_id', 1)
				dataNum = _db[collectionName].count_documents(query, limit=limit)
			else:
				data = _db[collectionName].find(query, { "message": 1, "_id": 0 }, batch_size=500).sort('_id', 1)
				dataNum = _db[collectionName].count_documents(query)

			if(dataNum > 0):
				record = data.next()
				tmpDF = pd.DataFrame()
				while(1):
					try:
						message = dict((k.lower(), v) for k, v in record["message"].items()) #convert key to lower case
						tmpDF = tmpDF.append({keyName:message[keyName]}, ignore_index=True)
						record = data.next()
					except StopIteration:
						break
				df = pd.concat([df, tmpDF], axis=1)
	#df = df.fillna(0) # Fill na with zero
	df = df.dropna(axis=0) # Remove row with na
	return df, df.to_numpy()

def training():
	global enable_anomaly
	config = getConfig()
	while(1):
		enable_anomaly = False
		print("Starting training")
		_, dataset = preprocessing({}, config["datasize"])
		clf = KNN()
		clf.fit(dataset)
		print("Saving model")
		dump(clf, 'clf.joblib')
		enable_anomaly = True
		time.sleep(config["training"] * 3600)

def prediction():
	global enable_anomaly, start
	px = 1/plt.rcParams['figure.dpi']
	config = getConfig()
	df = pd.DataFrame()
	while(1):
		if(enable_anomaly and config["enable"]):
			print("Processing prediction data")
			dummy_id = ObjectId.from_datetime(start)
			df_data,data = preprocessing({"_id": {"$gte": dummy_id}})
			start = datetime.datetime.today()
			clf = load('clf.joblib')
			y_train_scores = clf.decision_scores_
			std = np.std(y_train_scores)
			avg = np.average(y_train_scores)
			#var = np.var(y_train_scores)
			threshold = avg + std
			detect = False
			predict = []
			for idx, pred in enumerate(data):
				y_score = clf.decision_function(pred.reshape(1, -1))
				if(y_score[0] > threshold):
					predict.append(np.average(pred))
					detect = True
				else:
					predict.append(np.nan)
			if(detect):
				print("Anomaly detected")
				plt.figure(figsize=(1200*px, 800*px))
				plt.suptitle('Anomaly detection')
				for col in df_data.columns:
					plt.plot(df_data[col],"-o",label=col, alpha=0.7)
				df_data['anomaly'] = predict
				plt.plot(predict,"-rD",label="Anomaly", markersize=8)
				plt.grid()
				plt.legend(loc='best')
				buf = io.BytesIO()
				plt.savefig(buf) # Store image in buffered I/O

				tokens = getToken()
				message = "Anomaly detected"
				for token in tokens:
					#if token["ntime"] + datetime.datetime.timestamp(token["nlast_time"]) <= time.time():
						buf.seek(0) # Change the stream position to first byte
						notify_res = linenotify(buf,message, token["ntoken"])
						notify_status = "Failed"
						if(notify_res):
							notify_status = "Success"
						newLog(notify_status + ": " + message, token["ntoken"])
			time.sleep(10)

if __name__ == "__main__":
	t1=threading.Thread(target=training)
	t1.start()
	prediction()