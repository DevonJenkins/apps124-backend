from crypt import methods
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

#Show an app: GET api/apps/<id>
@apps.route('/<id>', methods=["GET"])
def show(id):
  app = App.query.filter_by(id=id).first()
  app_data = app.serialize()
  return jsonify(app=app_data), 200

#PUT api/apps/<id> 
@apps.route('/<id>', methods=["PUT"])
@login_required
def update(id):
  data = request.get_json()
  profile = read_token(request)
  app = App.query.filter_by(id=id).first()

  if app.profile_id != profile["id"]:
    return "Forbidden", 403
  
  for key in data:
    setattr(app, key, data[key])

  db.session.commit()
  return jsonify(app.serialize()), 200 