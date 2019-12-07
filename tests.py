"""Basic unittest class."""

import os
import unittest
from unittest.mock import patch

from procudo import app, get_user, get_file, gen_template, gen_ovpn_conf
from environs import EnvValidationError


class BasicTests(unittest.TestCase):
    def setUp(self):
        app.config['DEBUG'] = True
        envvars = {
            'ENV': None,
            'DEBUG': 'True',
            'LOGGING': 'DEBUG'
        }
        self.env = patch.dict('os.environ', envvars)

        self.app = app.test_client()
        self.app.testing = True
        self.assertEqual(app.debug, True)

        self.mock_user = {
            'username': 'test',
            'key': 'rsaABCDEFG',
            'cert': 'SOMECERT!@£'
        }

    def tearDown(self):
        pass

    def test_get_file_exists(self):
        with app.app_context():
            file = get_file('./data', 'ca.pem')
            self.assertNotEqual(EnvironmentError, file)

    def test_get_file_not_exists(self):
        with app.app_context():
            with self.assertRaises(EnvironmentError):
                get_file('./data', 'not_found.pem')

    def test_gen_template_not_exists(self):
        with app.app_context():
            with self.assertRaises(Exception):
                gen_template(ca='', tls='', user=self.mock_user, template='notfound.ovpn')

    def test_gen_ovpn_conf_user_not_found(self):
        with app.app_context():
            with self.assertRaises(Exception):
                gen_ovpn_conf('unknown')

    def test_gen_ovpn_conf_template_not_found(self):
        with app.app_context():
            with self.assertRaises(Exception):
                gen_ovpn_conf(None, profile='unknown')

    def test_get_user_not_found_is_none(self):
        self.assertEqual(get_user('unknown'), None)

    def test_root_page_endpoint(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 404)

    def test_default_profile_creation_endpoint(self):
        response = self.app.get('/v1/config/tom')
        self.assertEqual(response.status_code, 200)

    def test_named_profile_creation_endpoint(self):
        response = self.app.get('/v1/config/default/tom')
        self.assertEqual(response.status_code, 200)

    def test_envio_throws_exception(self):
        self.assertRaises(EnvValidationError)


class ProdEnvConfTests(unittest.TestCase):
    def setUp(self):
        app.config['DEBUG'] = False
        envvars = {
            'ENV': 'prod',
            'DEBUG': 'False',
            'LOGGING': 'DEBUG'
        }
        self.env = patch.dict('os.environ', envvars)

        self.app = app.test_client()
        self.app.testing = False
        self.assertEqual(app.debug, False)

    def tearDown(self):
        pass

    def test_is_prod_envio(self):
        with self.env:
            self.assertEqual(os.environ.get('ENV'), 'prod')
            self.assertEqual(os.environ.get('DEBUG'), 'False')
            self.assertEqual(os.environ.get('LOGGING'), 'DEBUG')


if __name__ == "__main__":
    unittest.main()
