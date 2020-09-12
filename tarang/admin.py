from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:vchip@localhost/tarang"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:vchip@127.0.0.1:3306/tarang"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Admin(db.Model):
	__tablename__= 'admin'
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
	remember_token = db.Column(db.String(128), 
		nullable=True)
	updated_at = db.Column(db.DateTime, 
		default=datetime.now)
	created_at = db.Column(db.DateTime,
		default=datetime.now)

	def __init__(self, name, email, password):
		self.name = name
		self.email = email
		self.password = password

	def __repr__(self):
		return '<Admin %r>' % self.name

# doc: Add table
# from admin import db
# db.create_all()  #to create table

# Add entries (insert) in table
# from admin import Admin
# admin = Admin('name','email','pass')
# db.session.add(admin)
# db.session.commit()

# Update entries in table
# update = Admin.query.filter_by(id=1).first()
# update.name = 'vchip'
# db.session.commit()

# Select data
# select = Admin.query.all()

