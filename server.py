#!/usr/bin/python
# -*- coding: utf-8 -*-

from pymongo import MongoClient
import redis
import json
import web

client = MongoClient(host='mongodb', port=27017)
db = client.mydb
coll = db.mycoll

cache = redis.Redis(host='rediska', port=6379)
cache.ping()

# For each end point there is a method that handles
# it in the HandleRequest class

urls = (r'/storage/?(?P<key>.+)?', 'HandleRequest')


# This class is used to handle requests

class HandleRequest:

    # Initialization code

    def __init__(self):

        # Set response content type (json) and
        # encoding (utf8) for all requests

        web.header('Content-Type', 'text/json; charset=utf-8')

    # --------------------------------------------

   # Handle HTTP GET

    def GET(self, key=None):
        if key is None:
            raise web.badrequest()
        else:

            answ = cache.get(key)
            response = {}
            if answ == None:

                db_doc = coll.find_one({'key': key})
                if db_doc == None:
                    response['Status'] = 'Not found'
                    raise web.notfound(json.dumps(response))
                else:
                    response['message'] = db_doc['msg']
                    response['Status'] = 'OK'
                    cache.set(key, response['message'])  # update chache
            else:

                if type(answ) is bytes:
                    response['message'] = answ.decode('utf-8')
                else:
                    response['message'] = answ
                response['Status'] = 'OK'

            return json.dumps(response)

    # --------------------------------------------

    # Handle HTTP POST

    def POST(self, key=None):
        if key is None:
            raise web.badrequest()
        else:
            response = {}
            obj_data = json.loads(web.data())
            db_doc = coll.find_one({'key': key})
            if db_doc == None:
                response['Status'] = 'Created'
                coll.insert_one({'key': key, 'msg': obj_data['message']})
            else:
                response['Status'] = 'OK'
                db_doc['msg'] = obj_data['message']
                if cache.exists(key):
                    cache.set(key, obj_data['message'])
            return json.dumps(response)

    # --------------------------------------------

    # Handle HTTP PUT

    def PUT(self, key=None):
        if key is None:
            raise web.badrequest()
        else:
            response = {}
            obj_data = json.loads(web.data())
            db_doc = coll.find_one({'key': key})
            if db_doc != None:
                db_doc['msg'] = obj_data['message']
                if cache.exists(key):
                    cache.set(key, obj_data['message'])
                response['Status'] = 'OK'
            else:
                response['Status'] = 'Not found'
                raise web.notfound(json.dumps(response))
            return json.dumps(response)

    # --------------------------------------------

    # Handle HTTP DELETE

    def DELETE(self, key=None):
        if key is None:
            raise web.badrequest()
        else:
            response = {}
            db_doc = coll.find_one({'key': key})
            if db_doc != None:
                coll.remove(db_doc)
                cache.delete(key)
                response['Status'] = 'OK'
            else:
                response['Status'] = 'Not found'
                raise web.notfound(json.dumps(response))
            return json.dumps(response)


    # --------------------------------------------

# Start web server

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()


			
