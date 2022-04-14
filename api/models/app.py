from datetime import datetime
from api.models.db import db 

class App(db.Model):
  __tablename__ = 'apps'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  appType = db.Column(db.String(100))
  description = db.Column(db.String(250))
  photo = db.Column(db.String(100))
  link = db.Column(db.String(100))
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))

  def __repr__(self):
    return f"Cat('{self.id}', '{self.name}'"

  def serialize(self):
    app = {c.name: getattr(self, c.name) for c in self.__table__.columns}
    return app