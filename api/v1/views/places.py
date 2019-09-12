#!/usr/bin/python3
"""function to create the route status"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places')
def places(city_id):
    """get City with his id"""
    for val in storage.all("City").values():
        if val.id == city_id:
            return jsonify(list(map(lambda v: v.to_dict(), val.places)))
    abort(404)


@app_views.route('/places/<place_id>')
def place_id(place_id):
    """get City with his id"""
    for val in storage.all("Place").values():
        if val.id == place_id:
            return jsonify(val.to_dict())
    abort(404)


@app_views.route('/places_search', methods=['POST'])
def place_search():
    """get City with his id"""
    list_places = []

    if request.is_json:
        data = request.get_json()
    else:
        msg = "Not a JSON"
        return jsonify({"error": msg}), 400

    if len(data) == 0:
        for val in storage.all("Place").values():
            list_places.append(val.to_dict())
    else:
        if "states" in data and len(data["states"]) > 0:
            for state_id in data["states"]:
                place = storage.get("State", state_id)
                for city in place.cities:
                    for pla in city.places:
                        list_places.append(pla.to_dict())

        if "cities" in data and len(data["cities"]) > 0:
            for city_id in data["cities"]:
                city = storage.get("City", city_id)
                for pla in city.places:
                    list_places.append(pla.to_dict())

        if "amenities" in data and len(data["amenities"]) > 0:
            list_amen = []
            list_pla = []
            for amen_id in data["amenities"]:
                list_amen.append(amen_id)
                amen = storage.get("Amenity", amen_id)
                for pla in amen.place_amenities:
                    list_pla.append(pla)
            for pla in list_pla:
                for amen_ids in pla.amenities:
                    if amen_ids.id in list_amen:
                        llaves = pla.to_dict()
                        del llaves["amenities"]
                        list_places.append(llaves)

    return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def places_delete(place_id):
    """delete a obj with his id"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    storage.close()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def place_create(city_id):
    """create city object"""
    City1 = storage.get("City", city_id)
    if City1 is None:
        abort(404)

    if request.is_json:
        data = request.get_json()
    else:
        msg = "Not a JSON"
        return jsonify({"error": msg}), 400

    if "user_id" not in data:
        msg = "Missing user_id"
        return jsonify({"error": msg}), 400

    user = storage.get("User", data["user_id"])
    if user is None:
        abort(404)

    if "name" not in data:
        msg = "Missing name"
        return jsonify({"error": msg}), 400

    data.update({'city_id': city_id})
    place = Place(**data)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def place_update(place_id):
    """update City"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    if request.is_json:
        data = request.get_json()
    else:
        msg = "Not a JSON"
        return jsonify({"error": msg}), 400

    for k, v in data.items():
        if k not in ["id", "created_at", "updated_at",
                     "city_id", "user_id"]:
            setattr(place, k, v)

    storage.save()
    return jsonify(place.to_dict()), 200
