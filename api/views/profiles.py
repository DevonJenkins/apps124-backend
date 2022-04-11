from crypt import methods
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