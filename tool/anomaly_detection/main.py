import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pyod.models.knn import KNN
from joblib import dump, load
import time, threading, datetime, io, os
from bson.objectid import ObjectId
from config import Config
from notify import linenotify
from db import MySQL, MongoDB

enable_anomaly = False
start = int(time.time())
model_folder = "models"

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

def getMacAddress():
	config = getConfig()
	with initMongo() as _client:
		_db = _client[Config.MONGODB_DATA_COLLECTION]
		res = []
		for topic in config["detections"]:
			res.append({
				"topic": topic,
				"MAC": _db[topic].distinct('message.MAC')
			})
	return res

def getRoomName(mac):
	with initMySQL() as _cur:
		_cur.execute("SELECT r.rname FROM board b JOIN room r ON b.rid = r.rid WHERE b.bomac = %s",(mac,))
		return _cur.fetchone()["rname"]

def preprocessing(topic,mac, ts=None,limit=None):
	config = getConfig()
	df = pd.DataFrame()
	query = {"message.MAC": mac}
	if(ts):
		query["created_at"] = { "$gte": ts } 
	with initMongo() as _client:
		_db = _client[Config.MONGODB_DATA_COLLECTION]
		collectionName = topic
		print("Processing: ", collectionName, mac, ts)
		if(limit != None and int(limit) > 0):
			data = _db[collectionName].find(query, { "message": 1, "_id": 0 }, limit=limit, batch_size=500).sort('_id', 1)
			dataNum = _db[collectionName].count_documents(query, limit=limit)
		else:
			data = _db[collectionName].find(query, { "message": 1, "_id": 0 }, batch_size=500).sort('_id', 1)
			dataNum = _db[collectionName].count_documents(query)

		if(dataNum > 0):
			record = data.next()
			tmpDF = pd.DataFrame()
			# Get list for key if type is int
			keyList = [k for k, v in record["message"].items() if(type(v) == int)]
			while(1):
				try:
					tmp = {}
					for key in keyList:
						tmp[key.lower()] = record["message"][key]
					tmpDF = tmpDF.append(tmp, ignore_index=True)
					record = data.next()
				except StopIteration:
					break
			df = tmpDF
	#df = df.fillna(0) # Fill na with zero
	df = df.dropna(axis=0) # Remove row with na
	return df, df.to_numpy()

def training():
	global enable_anomaly, model_folder
	config = getConfig()
	while(1):
		enable_anomaly = False
		macAddress = getMacAddress()
		print("Starting training")
		for address in macAddress:
			for mac in address["MAC"]:
				_, dataset = preprocessing(address["topic"], mac, None, config["datasize"])
				clf = KNN()
				clf.fit(dataset)
				print("Saving model")
				dump(clf, model_folder + "/" +address["topic"]+"_"+mac+'.joblib')
		enable_anomaly = True
		time.sleep(config["training"] * 3600)

def prediction():
	global enable_anomaly, start, model_folder
	px = 1/plt.rcParams['figure.dpi']
	config = getConfig()
	df = pd.DataFrame()
	while(1):
		if(enable_anomaly and config["enable"]):
			macAddress = getMacAddress()
			for address in macAddress:
				for mac in address["MAC"]:
					print("Processing prediction data")
					path = model_folder + "/" +address["topic"]+"_"+mac+'.joblib'
					if(os.path.isfile(path)):
						df_data, data = preprocessing(address["topic"], mac, start)
						start = int(time.time())
						clf = load(path)
						y_train_scores = clf.decision_scores_
						std = np.std(y_train_scores)
						avg = np.average(y_train_scores)
						#var = np.var(y_train_scores)
						threshold = avg + std
						detect = False
						predict = []
						print(data)
						for idx, pred in enumerate(data):
							y_score = clf.decision_function(pred.reshape(1, -1))
							print(y_score[0])
							if(y_score[0] > threshold):
								predict.append(np.average(pred))
								detect = True
							else:
								predict.append(np.nan)
						if(detect):
							print("Anomaly detected")
							plt.figure(figsize=(1200*px, 800*px))
							plt.suptitle('Anomaly detection '+ address["topic"])
							for col in df_data.columns:
								plt.plot(df_data[col],"-o",label=col, alpha=0.7)
							df_data['anomaly'] = predict
							plt.plot(predict,"-rD",label="Anomaly", markersize=8)
							plt.grid()
							plt.legend(loc='best')
							buf = io.BytesIO()
							plt.savefig(buf) # Store image in buffered I/O

							tokens = getToken()
							room = getRoomName(mac)
							message = "Anomaly detected "+ address["topic"] + "\nRoom: " + room + "\nMac address: " + mac
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