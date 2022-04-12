from crypt import methods
from wsgiref.util import request_uri
from flask import Blueprint, jsonify, request
from api.middleware import login_required, read_token

from api.models.db import db
from api.models.badge import Badge

badges = Blueprint('badges', 'badges')

#Create badges POST api/badges/
@badges.route('/', methods=['POST'])
@login_required
def create():
  data = request.get_json()
  profile = read_token(request)
  data["profile_id"] = profile["id"]

  badge = Badge(**data)
  db.session.add(badge)
  db.session.commit()
  return jsonify(badge.serialize()), 201

#Index badges: GET/api/badges/
@badges.route('/', methods=['GET'])
def index():
  badges = Badge.query.all()
  return jsonify([badge.serialize() for badge in badges]), 201 

#Show a badge
@badges.route('/<id>', methods=["GET"])
def show(id):
  badge = Badge.query.filter_by(id=id).first()
  return jsonify(badge.serialize()), 200

#Update a badges: PUT api/badges/<id> 
@badges.route('/<id>', methods=["PUT"])
@login_required
def update(id):
  data = request.get_json()
  profile = read_token(request)
  badge = Badge.query.filter_by(id=id).first()

  if badge.profile_id != profile["id"]:
    return "Forbidden", 403
  
  for key in data:
    setattr(badge, key, data[key])

  db.session.commit()
  return jsonify(badge.serialize()), 200 

#Delete a badge: DELETE api/badges/<id>
@badges.route('/<id>', methods=["DELETE"])
@login_required
def delete(id):
  profile = read_token(request)
  badge = Badge.query.filter_by(id=id).first()

  if badge.profile_id != profile["id"]:
    return "Forbidden", 403

  db.session.delete(badge)
  db.session.commit()
  return jsonify(message="Delete Successful"), 200 

