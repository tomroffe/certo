"""Flask config class."""

import os


class Config:
    """Set Flask configuration vars."""

    # General Config
    SESSION_COOKIE_NAME = 'procudo'
    ENDPOINT = os.environ.get('ENDPOINT')
    PORT = 1194
    PROTOCAL = 'udp'
    DATA_PATH = './data'
    CLIENT_PATH = 'clients'
    CA_CERT_FILENAME = 'ca.pem'
    TLS_KEY_FILENAME = 'ta.key'


class ProdConfig(Config):
    DEBUG = False
    TESTING = False

    ENDPOINT = os.environ.get('ENDPOINT'),
    PORT = os.environ.get('PORT')
    PROTOCAL = os.environ.get('PROTOCAL')
    DATA_PATH = os.environ.get('DATA_PATH')
    CLIENT_PATH = os.environ.get('CLIENT_PATH')
    CA_CERT_FILENAME = os.environ.get('CA_CERT_FILENAME')
    TLS_KEY_FILENAME = os.environ.get('TLS_KEY_FILENAME')
    SECRET_KEY = os.environ.get('SECRET_KEY')
