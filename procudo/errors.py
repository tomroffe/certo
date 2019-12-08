import logging
from flask import jsonify
from flask import make_response


def notfound(error):
    """Serve 404 Error"""
    logging.error("Template Not Found", exc_info=True)
    response = jsonify(status=404, error="404: Resource Not Found")
    return make_response(response, 404)
