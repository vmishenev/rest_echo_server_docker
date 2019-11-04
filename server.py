#!/usr/bin/env python

from pymongo import MongoClient
import socket
import logging
import redis
import json

# add filemode="w" to overwrite
#logging.basicConfig(filename="/var/log/server.log", level=logging.INFO)





client = MongoClient(host='mongodb',username="user", password="password", authSource="mydb", port=27017)
db=client.mydb
coll = db.mycoll

sock = socket.socket()
sock.bind(('', 9091))
sock.listen(1)
conn, addr = sock.accept()

print ('connected:', addr)
cache = redis.Redis(host='rediska', port=6379)
cache.ping()

while True:
    data = conn.recv(1024)

    if not data:
        break
    response = { }
    obj_data = {'action': 1 }
    try:
        obj_data = json.loads(data)
    except ValueError as e:
        response["Status"] = "Bad Request"
    
    if obj_data["action"] == "get":
        answ = cache.get(obj_data["key"])
        
        if answ == None or obj_data["no-chache"]:
            
            db_doc = coll.find_one({"key": obj_data["key"]})
            if db_doc == None:
               response["Status"] = "Not found"
            else:
               response["message"] = db_doc["msg"].decode('utf-8')
               response["Status"] = "OK"
               cache.set(obj_data["key"], response["message"]) #update chache
        else:

            if type(answ) is bytes:
                response["message"] = answ.decode('utf-8')
            else:            
                response["message"] = answ
            response["Status"] = "OK"
            print ('get:', response["message"])
            
    if obj_data["action"] == "put":
        if cache.exists(obj_data["key"]) :
            response["Status"] = "Created" 
        else:
            response["Status"] = "OK"
        coll.insert_one({"key":obj_data["key"], "msg":obj_data["message"]})
        #cache.set(obj_data["key"], obj_data["message"])
    if obj_data["action"] == "delete":
        db_doc = coll.find_one({"key": obj_data["key"]})
        if db_doc != None :    
            coll.remove(db_doc)
            cache.delete(obj_data["key"] )
            response["Status"] = "OK" 
        else:
            response["Status"] = "Not found"

    json_string = json.dumps(response)
    conn.send(json_string.encode('utf-8'))


    #logging.info(data)
conn.close()
