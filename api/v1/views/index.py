#!/usr/bin/python3
"""function to create the route status"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from flasgger import swag_from


@app_views.route('/status')
@swag_from('./apidocs/status.yml')
def status():
    """status render template for json"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
@swag_from('./apidocs/stats.yml')
def stats():
    """status render template for json"""
    dict_objs = {'amenities': 'Amenity', 'cities': 'City', 'places': 'Place',
                 'reviews': 'Review', 'states': 'State', 'users': 'User'}
    new_dict = {}
    for k, v in dict_objs.items():
        new_dict[k] = storage.count(v)
    return jsonify(new_dict)
