#!/usr/bin/env python

from pymongo import MongoClient
import socket
import logging
import redis
import json
import web

# add filemode="w" to overwrite
#logging.basicConfig(filename="/var/log/server.log", level=logging.INFO)





client = MongoClient(host='mongodb', port=27017)
db=client.mydb
coll = db.mycoll


cache = redis.Redis(host='rediska', port=6379)
cache.ping()


# For each end point there is a method that handles
# it in the HandleRequest class
urls = (r'/storage/?(?P<key>.+)?', 'HandleRequest')

# This class is used to handle requests
class HandleRequest():
    
    # Initialization code
    def __init__(self):
        # Set response content type (json) and 
        # encoding (utf8) for all requests
        web.header('Content-Type', 'text/json; charset=utf-8')
       
    #--------------------------------------------
                               
   # Handle HTTP GET
    def GET(self, key=None):
       # If no id is provided list all cars
        if key is None:
           raise web.badrequest()
        # Otherwise send back the requested car object
        else:
            answ = cache.get(key)
            response = { }
            if answ == None:
                
                db_doc = coll.find_one({"key":key})
                if db_doc == None:
                   response["Status"] = "Not found"
                else:
                   response["message"] = db_doc["msg"]
                   response["Status"] = "OK"
                   cache.set(key, response["message"]) #update chache
            else:

                if type(answ) is bytes:
                    response["message"] = answ.decode('utf-8')
                else:            
                    response["message"] = answ
                response["Status"] = "OK"

            return json.dumps(response)
 
    #--------------------------------------------
                
    # Handle HTTP POST
    def POST(self, key=None):
        if key is None:
            raise web.badrequest()
        else:
            raise web.badrequest()
    
    #--------------------------------------------
 
    # Handle HTTP PUT
    def PUT(self, key=None):
        if key is None:
            raise web.badrequest()
        else:
            response = {}
            if cache.exists(key) :
                response["Status"] = "Created" 
            else:
                response["Status"] = "OK"
            obj_data = json.loads(web.data())
            coll.insert_one({"key":key, "msg":obj_data["message"]})
            return json.dumps(response)
    
    #--------------------------------------------
 
    # Handle HTTP DELETE
    def DELETE(self, key=None):
        # You can not delete a car if id does not exist
        if key is None:
            raise web.badrequest()
        else:
            response = {}
            db_doc = coll.find_one({"key": key})
            if db_doc != None :    
                coll.remove(db_doc)
                cache.delete(key )
                response["Status"] = "OK" 
            else:
                response["Status"] = "Not found"
            return json.dumps(response)
 
    #--------------------------------------------
 
# Start web server
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
