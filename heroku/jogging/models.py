from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

class Users (db.Model):
    id =db.Column(db.Integer,primary_key=True)
    Name= db.Column(db.String)
    Gender=db.Column(db.String)
    Adress=db.Column(db.String)
    weight= db.Column(db.Float)
    height= db.Column(db.Float)
    Age= db.Column(db.DateTime)
    def __repr__(self):
        return "< Users {} {} {} {} {} >".format(self.id, self.Name, self.weight,self.height,self.Gender)
class PointGroup(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    u_id=db.Column(db.Integer,db.ForeignKey("users.id"))
    Name=db.Column(db.String)
    def __repr__(self):
        return "< PointGroup {} {} {} >".format(self.id,self.u_id,self.Name)

class Points(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    g_id=db.Column(db.Integer,db.ForeignKey("point_group.id"))
    lng=db.Column(db.Float)
    lat=db.Column(db.Float)
    def __repr__(self):
        return "< Points {} {} {}>".format(self.g_id,self.lng, self.lat)
class traindata(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    u_id=db.Column(db.Integer,db.ForeignKey("users.id"))
    X=db.Column(db.ARRAY(db.Float))
    y=db.Column(db.Integer)
    def __repr__(self):
        return "< traindata {} {} {}>".format(self.u_id,self.X, self.y)

def parse_records(db_data):
    parsed_list = []
    for record in db_data:
        parsed_record = record.__dict__
        del parsed_record["_sa_instance_state"]
        parsed_list.append(parsed_record)
    return parsed_list
