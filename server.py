#!/usr/bin/env python


import json
import web
import hashlib
import redis
import requests



cache = redis.Redis(host='rediska', port=6379)
cache.ping()


# For each end point there is a method that handles
# it in the HandleRequest class
urls = (r'/storage/?(?P<key>.+)?', 'HandleRequest')

def get_server(key):
   num = abs(hash(key)) % 2
   return ["http://localhost:8083", "http://localhost:8083" ][num]

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
                r = requests.delete(get_server(key) +"/storage/" + key)
                response = r.json()
                if response["Status"] == "OK":
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
            obj_data = json.loads(web.data())
            r = requests.put(get_server(key) +"/storage/"+key, json=obj_data)
            return e
    
    #--------------------------------------------
 
    # Handle HTTP DELETE
    def DELETE(self, key=None):
        # You can not delete a car if id does not exist
        if key is None:
            raise web.badrequest()
        else:
            response = {}
            cache.delete(key )
            return requests.delete(get_server(key) +"/storage/" + key)
 
    #--------------------------------------------
 
# Start web server
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
