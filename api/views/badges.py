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
