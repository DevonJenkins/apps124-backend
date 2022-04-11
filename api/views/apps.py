from flask import Blueprint, jsonify, request
from api.middleware import login_required, read_token

from api.models.db import db
from api.models.app import App

apps = Blueprint('apps', 'apps')

#Create an app: POST api/apps
@apps.route('/', methods=["POST"])
@login_required
def create():
  data = request.get_json()
  profile = read_token(request)
  data["profile_id"] = profile["id"]
  app = App(**data)
  db.session.add(app)
  db.session.commit()

  return jsonify(app.serialize()), 201 

#Index apps: GET api/apps 
@apps.route('/', methods=["GET"])
def index():
  apps = App.query.all()
  return jsonify([app.serialize() for app in apps]), 200   