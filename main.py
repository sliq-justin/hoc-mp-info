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

if __name__ == '__main__':
    port = int(environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
