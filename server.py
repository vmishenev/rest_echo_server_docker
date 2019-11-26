#!/usr/bin/python
# -*- coding: utf-8 -*-

from pymongo import MongoClient
import logging
import redis
import json
import web

logging.basicConfig(filename='/var/log/server.log', level=logging.INFO)

client = MongoClient(host='mongodb', port=27017)
db = client.mydb
coll = db.mycoll

cache = redis.Redis(host='rediska', port=6379)
cache.ping()

# For each end point there is a method that handles
# it in the HandleRequest class

urls = (r'/storage/?(?P<key>.+)?', 'HandleRequest')


class HandleRequest:

    """This class is used to handle requests"""

    def __init__(self):
        """Initialization code.
        Set response content type (json) and
        encoding (utf8) for all requests"""

        web.header('Content-Type', 'text/json; charset=utf-8')

    # --------------------------------------------

    def GET(self, key=None):
        """ Handle HTTP GET """

        logging.info('http-get for key %s', key)
        if key is None:
            raise web.badrequest()
        else:

            answ = cache.get(key)
            logging.debug('get for key %s', key)
            response = {}
            if answ == None:
                logging.warning('no data in cache for key %s', key)
                db_doc = coll.find_one({'key': key})
                if db_doc == None:
                    response['Status'] = 'Not found'
                    logging.error('no data in database for key %s', key)
                    raise web.notfound(json.dumps(response))
                else:
                    response['message'] = db_doc['msg']
                    response['Status'] = 'OK'
                    logging.debug('update cache key %s', key)
                    cache.set(key, response['message'])  # update chache
            else:

                if isinstance(answ, bytes):
                    response['message'] = answ.decode('utf-8')
                else:
                    response['message'] = answ
                response['Status'] = 'OK'

            return json.dumps(response)

    # --------------------------------------------

    def POST(self, key=None):
        """ Handle HTTP POST """

        logging.info('http-POST for key %s', key)
        if key is None:
            raise web.badrequest()
        else:
            response = {}
            obj_data = json.loads(web.data())
            db_doc = coll.find_one({'key': key})
            if db_doc == None:
                response['Status'] = 'Created'
                logging.debug('inser to db key %s', key)
                coll.insert_one({'key': key, 'msg': obj_data['message'
                                ]})
            else:
                response['Status'] = 'OK'
                db_doc['msg'] = obj_data['message']
                if cache.exists(key):
                    logging.debug('update cache key %s', key)
                    cache.set(key, obj_data['message'])
            return json.dumps(response)

    # --------------------------------------------

    def PUT(self, key=None):
        """ Handle HTTP PUT """

        logging.info('http-PUT for key %s', key)
        if key is None:
            raise web.badrequest()
        else:
            response = {}
            obj_data = json.loads(web.data())
            db_doc = coll.find_one({'key': key})
            if db_doc != None:
                db_doc['msg'] = obj_data['message']
                if cache.exists(key):
                    logging.debug('update cache key %s', key)
                    cache.set(key, obj_data['message'])
                response['Status'] = 'OK'
            else:
                response['Status'] = 'Not found'
                logging.error('no data in database for key %s', key)
                raise web.notfound(json.dumps(response))
            return json.dumps(response)

    # --------------------------------------------

    def DELETE(self, key=None):
        """ Handle HTTP DELETE """

        logging.info('http-delete for key %s', key)
        if key is None:
            raise web.badrequest()
        else:
            response = {}
            db_doc = coll.find_one({'key': key})
            if db_doc != None:
                logging.debug('remove from db and cache key %s', key)
                coll.remove(db_doc)
                cache.delete(key)
                response['Status'] = 'OK'
            else:
                response['Status'] = 'Not found'
                logging.error('no data in database for key %s', key)
                raise web.notfound(json.dumps(response))
            return json.dumps(response)


    # --------------------------------------------

# Start web server

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()


			
