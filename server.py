#!/usr/bin/python
# -*- coding: utf-8 -*-

from pymongo import MongoClient
import redis
import json
import web

# For each end point there is a method that handles
# it in the HandleRequest class

urls = (r'/storage/?(?P<key>.+)?', 'HandleRequest')


#

class HandleRequestCntr:

    """This class is used to handle requests"""

    def __init__(self):

        # Set response content type (json) and
        # encoding (utf8) for all requests

        web.header('Content-Type', 'text/json; charset=utf-8')
        self.service = Service()

    # --------------------------------------------

   # Handle HTTP GET

    def GET(self, key=None):
        if key is None:
            raise web.badrequest()
        else:
            answ = self.service.get(key)
            response = {}
            if answ == None:
                response['Status'] = 'Not found'
                raise web.notfound(json.dumps(response))
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
            res = self.service.add(key, obj_data['message'])
            if res:
                response['Status'] = 'Created'
            else:
                response['Status'] = 'OK'
            return json.dumps(response)

    # --------------------------------------------

    # Handle HTTP PUT

    def PUT(self, key=None):
        if key is None:
            raise web.badrequest()
        else:
            response = {}
            obj_data = json.loads(web.data())
            res = self.service.service.edit(key, obj_data['message'])
            if res:
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
            if service.delete(key):
                response['Status'] = 'OK'
            else:
                response['Status'] = 'Not found'
                raise web.notfound(json.dumps(response))
            return json.dumps(response)


    # --------------------------------------------

class Service:

    def __init__(self):
        self.rep = Repository()

    def delete(self, key):
        db_doc = self.rep.findDocDb(key)
        if db_doc != None:
            self.rep.removeFromDb(db_doc)
            self.rep.removeFromChache(key)
            return True
        else:
            return False

    def add(self, key, msg):
        db_doc = self.rep.findDocDb(key)
        if db_doc == None:
            self.rep.insertDb(key, msg)
            return True  # added
        else:
            db_doc['msg'] = msg
            if self.rep.findChache(key) != None:
                self.rep.setChache(key, msg)
            return False

    def edit(self, key, msg):
        db_doc = self.rep.findDocDb(key)
        if db_doc == None:
            return False  # added
        else:
            db_doc['msg'] = msg
            if self.rep.findChache(key) != None:
                self.rep.setChache(key, msg)
            return True

    def get(self, key):
        msg = self.rep.findChache(key)
        if msg == None:
            db_doc = self.rep.findDocDb(key)
            setChache(key, db_doc['msg'])  # upd chache
            return db_doc['msg']  # added
        else:
            return msg


class Repository:

    def __init__(self):
        self.client = MongoClient(host='mongodb', port=27017)
        self.db = client.mydb
        self.coll = db.mycoll

        self.cache = redis.Redis(host='rediska', port=6379)
        self.cache.ping()

    def insertDb(key, msg):
        if findDocDb(key) == None:
            self.coll.insert_one({'key': key, 'msg': msg})
            return True
        return False

    def setChache(key, msg):
        return self.cache.set(key, msg)

    def findChache(key):
        answ = self.cache.get(key)
        if isinstance(answ, bytes):
            answ.decode('utf-8')
        else:
            return answ

    def findDocDb(db_doc):
        return self.coll.find_one({'key': key})

    def removeFromDb(db_doc):
        self.coll.remove(db_doc)

    def removeFromChache(key):
        self.cache.delete(key)

    def removeFromDb(db_doc):
        self.coll.remove(db_doc)

    def removeFromChache(key):
        self.cache.delete(key)


# Start web server

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()


			
