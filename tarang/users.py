from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:vishu@127.0.0.1:3306/tarang"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Users(db.Model):
	__tablename__= 'users'
	id = db.Column(db.Integer, 
		primary_key=True)
	name = db.Column(db.String(64), 
		index=False, 
		nullable=False)
	email = db.Column(db.String(80),
		index=True, 
		unique=True, 
		nullable=False)
	password = db.Column(db.String(128), 
		nullable=False)
	phone = db.Column(db.Integer(),
		nullable=False)
	email_verified = db.Column(db.SmallInteger(),
		default=0)
	admin_verified = db.Column(db.SmallInteger(),
		default=0)
	google_provider_id = db.Column(db.String(128), 
		nullable=True)
	facebook_provider_id = db.Column(db.String(128), 
		nullable=True)
	batch_ids = db.Column(db.String(128), 
		nullable=True)
	remember_token = db.Column(db.String(128), 
		nullable=True)
	updated_at = db.Column(db.DateTime, 
		default=datetime.now)
	created_at = db.Column(db.DateTime,
		default=datetime.now)

	def __init__(self, name, email, password, phone=1234567890, google_provider_id=None,
	 facebook_provider_id=None, batch_ids=None, remember_token=None):
		self.name = name
		self.email = email
		self.password = password
		self.phone = phone
		if(google_provider_id):
			self.google_provider_id = google_provider_id
		if(facebook_provider_id):
			self.facebook_provider_id = facebook_provider_id
		if(batch_ids):
			self.batch_ids = batch_ids
		if(remember_token):
			self.remember_token = remember_token

	def __repr__(self):
		return '<User %r>' % self.name
