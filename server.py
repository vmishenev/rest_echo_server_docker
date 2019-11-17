#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import web
import hashlib
import redis
import requests

cache = redis.Redis(host='rediska', port=6379)
cache.ping()

list_servers = ['http://localhost:8083', 'http://localhost:8083']

# For each end point there is a method that handles
# it in the HandleRequest class

urls = (r'/storage/?(?P<key>.+)?', 'HandleRequest')


def get_server(key):
    num = abs(hash(key)) % len(list_servers)
    return list_servers[num]


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
                r = requests.get(get_server(key) + '/storage/' + key)
                response = r.json()
                if response['Status'] == 'OK':
                    cache.set(key, response['message'])  # update chache
            else:

                if isinstance(answ, bytes):
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
            obj_data = json.loads(web.data())
            r = requests.post(get_server(key) + '/storage/' + key,
                              json=obj_data)
            return e

    # --------------------------------------------

    # Handle HTTP PUT

    def PUT(self, key=None):
        if key is None:
            raise web.badrequest()
        else:
            obj_data = json.loads(web.data())
            r = requests.put(get_server(key) + '/storage/' + key,
                             json=obj_data)
            return e

    # --------------------------------------------

    # Handle HTTP DELETE

    def DELETE(self, key=None):
        if key is None:
            raise web.badrequest()
        else:
            cache.delete(key)
            return requests.delete(get_server(key) + '/storage/' + key)


    # --------------------------------------------

# Start web server

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()

