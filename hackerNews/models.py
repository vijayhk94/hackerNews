from hackerNews import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.sql import func



@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True, nullable=False)
	email = db.Column(db.String(50), unique=True, nullable=False)	
	image_file = db.Column(db.String(50), nullable=False, default='default.jpg')
	password = db.Column(db.String(100), nullable=False)
	#tests = db.relationship('Test', backref='author', lazy=True)
	#posts = db.relationship('Post', backref='author', lazy=True)
	is_admin = db.Column(db.Integer, nullable=False, default=0)

	
	def get_id(self):
		return (self.id)

	def __repr__(self):
		return "User('{}', '{}', '{}')".format(self.username, self.email, self.image_file)

class HnItem(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.Unicode(200, collation='utf8_bin'), nullable=False)
	url = db.Column(db.Unicode(200, collation='utf8_bin'), nullable=False)
	hnUrl = db.Column(db.Unicode(200, collation='utf8_bin'), nullable=False)
	postedHoursBefore = db.Column(db.Integer, nullable=False)
	upvotes = db.Column(db.Integer, nullable=False, default=0)
	comments = db.Column(db.Integer, nullable=False, default=0)
	def __init__(self, id, title, url, hnUrl, postedHoursBefore, upvotes, comments):
		self.title = title
		self.id = id
		self.url = url
		self.hnUrl = hnUrl
		self.postedHoursBefore = postedHoursBefore
		self.upvotes = upvotes
		self.comments = comments
	def __repr__(self):
		return "HnItem('{}','{}','{}','{}','{}','{}','{}')".format(self.id,self.title, self.url, self.hnUrl, self.postedHoursBefore, self.upvotes, self.comments)

class Bookmarks(db.Model):
	__tablename__ = 'Bookmarks'
	id = db.Column(db.Integer, primary_key=True, nullable = False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	news_id = db.Column(db.Integer, db.ForeignKey('hn_item.id'), nullable=False)
	def __init__(self, user_id, news_id):
		self.news_id = news_id
		self.user_id = user_id