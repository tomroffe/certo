
import json
import logging

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import Response
from flask_cors import CORS

import os
import re

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
cors = CORS(app)

data_path = './data'
ca_cert = 'ca.pem'
tls_key = 'ta.key'
client_path = '{}/clients'.format(data_path)
keys, certs = [], []

def get_user(username):
    for root, dirs, files in os.walk(client_path):
        for filename in files:
            match = re.search(r'{}-key'.format(username), filename)
            if match:
                key = get_file(root, filename)
                cert = get_file(root, filename.replace('-key', ''))
                user = {
                    'username': username,
                    'key': key,
                    'cert': cert
                }
                return user

def get_file(path, filename):
    try:
        f = open("{}/{}".format(path, filename), 'r')
        data = f.read()
        return data
    except Exception:
        logging.error("Error Reading File", exc_info=True)
    finally:
        f.close()


@app.route("/gen/<profile>/<user>")
def gen_ovpn_conf(profile, user):
    ca = get_file(data_path, ca_cert)
    tls = get_file(data_path, tls_key)
    user = get_user(user)
    
    template = '{}.ovpn'.format(profile)
    body = render_template(template, 
                            ca_cert=ca.strip(), 
                            tls_key=tls.strip(), 
                            user_cert=user['cert'].strip(),  
                            user_key=user['key'].strip()) 

    return Response(body, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


