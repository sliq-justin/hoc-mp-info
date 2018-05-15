import xmltodict
import json
import urllib
import sys

from os import environ

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/member/<member_id>')
def get_member_information(member_id):
    if len(member_id) < 2:
        return json.dumps({message:"invalid member number"})
    else:
        link = "http://www.ourcommons.ca/Parliamentarians/en/members/%s/ExportRoles?current=True&output=XML" % member_id
        return json.dumps(xmltodict.parse(urllib.urlopen(link).read()))

@app.route('/update/<member_id>')
def update_cached_member_data(member_id):
    return json.dumps({"message":"/update/{member_id} route in progress"})

@app.route('/cache_test/<item_id>')
def mock_cache_check_and_return(item_id):
    # check db for requested item
    # if it exists:
    #   return it
    # if it does not exist:
    #   fetch from remote
    #   return it
    #   store in db

    return json.dumps({"message":"/cache_test/{item_id} route in progress"})

if __name__ == '__main__':
    port = int(environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
