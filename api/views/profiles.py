from crypt import methods
from email import message
from nis import cat
from flask import Blueprint, jsonify, request 
from api.middleware import login_required, read_token

from api.models.db import db
from api.models.profile import Profile

profiles = Blueprint('profiles', 'profiles')

# GET api/profiles
@profiles.route('/', methods=["GET"])
def index():
  profiles = Profile.query.all()
  return jsonify([profile.serialize() for profile in profiles]), 200

# GET api/profiles/<id> 

@profiles.route('/<id>', methods=["GET"])
def show(id):
  profile = Profile.query.filter_by(id=id).first()
  return jsonify(profile.serialize()), 200

#Update profiles: PUT api/profiles/<id> 
@profiles.route('/<id>', methods=["PUT"])
@login_required
def update(id):
  data = request.get_json()
  profile = read_token(request)
  user_profile = Profile.query.filter_by(id=id).first()

  if user_profile.id != profile["id"]:
    return "Forbidden", 403

  for key in data:
    setattr(user_profile, key, data[key])

  db.session.commit()
  return jsonify(user_profile.serialize()), 200

#Delete a badge: DELETE api/badges/<id>
@profiles.route('/<id>', methods=["DELETE"])
@login_required
def delete(id):
  profile = read_token(request)
  user_profile = Profile.query.filter_by(id=id).first()

  if user_profile.id != profile["id"]:
    return "Forbidden", 403

  db.session.delete(user_profile)
  db.session.commit()
  return jsonify(message="Delete Successful"), 200 

