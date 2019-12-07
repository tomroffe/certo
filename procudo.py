
import os
import re
import logging
from logging.config import dictConfig
from environs import Env, EnvValidationError

from flask import Flask
from flask import abort
from flask import render_template
from flask import Response
from jinja2.exceptions import TemplateNotFound

from errors import notfound

env = Env()
try:
    log_level = env.str("LOGGING")
except EnvValidationError:
    # https://docs.python.org/3.7/library/logging.html#logging-levels
    log_level = 'INFO'
finally:
    logging.info("Setting LOGGING={}".format(log_level))


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': log_level,
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
app.register_error_handler(404, notfound)
if app.config["ENV"] == "prod":
    app.config.from_object("config.ProdConfig")
else:
    app.config.from_object("config.Config")

keys, certs = [], []


def get_user(username):
    path = '{}/{}'.format(app.config['DATA_PATH'], app.config['CLIENT_PATH'])
    for root, dirs, files in os.walk(path):
        for filename in files:
            match = re.search(r'{}-key'.format(username), filename)
            if match:
                key = get_file(root, filename)
                cert = get_file(root, filename.replace('-key', ''))
                user = {
                    'username': username,
                    'key': key.rstrip(),
                    'cert': cert.rstrip()
                }
                return user


def get_file(path, filename):
    file_path = "{}/{}".format(path, filename)
    try:
        f = open(file_path, mode='r')
    except EnvironmentError as e:
        logging.error("File Not Found : '{}'".format(path), exc_info=True)
        raise EnvironmentError(e)
    else:
        try:
            data = f.read()
        finally:
            f.close()

    return data.strip()


def gen_template(ca, tls, user, template):
    try:
        body = render_template(template,
                               endpoint=app.config['ENDPOINT'],
                               endpoint_port=app.config['PORT'],
                               endpoint_protocal=app.config['PROTOCAL'],
                               ca_cert=ca,
                               tls_key=tls,
                               user_cert=user['cert'],
                               user_key=user['key'])
        return body
    except TemplateNotFound:
        raise Exception


@app.route("/v1/config/<string:profile>/<string:user>")
@app.route("/v1/config/<string:user>")
def gen_ovpn_conf(user, profile='default'):
    """Generate & serve user config file"""
    ca = get_file(app.config['DATA_PATH'], app.config['CA_CERT_FILENAME'])
    tls = get_file(app.config['DATA_PATH'], app.config['TLS_KEY_FILENAME'])
    user = get_user(user)
    template = '{}.ovpn'.format(profile)

    if user is not None:
        profile = gen_template(ca, tls, user, template)
        return Response(profile, mimetype='application/x-openvpn-profile')
    else:
        return abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, ssl_context='adhoc')
