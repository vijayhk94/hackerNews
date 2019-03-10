import os
import secrets
from flask import render_template, url_for, flash, redirect, json,request, abort,jsonify, json, Markup
from hackerNews import app, db, bcrypt, mysql
from hackerNews.forms import RegistrationForm, LoginForm
from hackerNews.models import User, HnItem, Bookmarks
from hackerNews.HnScraper import HnScraper
from hackerNews.HnItemDao import HnItemDao
from flask_login import login_user, current_user, logout_user, login_required
from flask_json import FlaskJSON, JsonError, json_response, as_json
import re

		

@app.route("/")
def main():
	#tests = Test.query.order_by(Test.date_posted.desc())
	return render_template('allnews.html')

@app.route("/user/<string:username>")
def user_posts(username):	
	page = request.args.get('page', 1, type=int)
	user = User.query.filter_by(username=username).first_or_404()
	posts = Post.query\
				.filter_by(author=user)\
				.order_by(Post.date_posted.desc())\
				.paginate(page=page, per_page=5)
	return render_template('user_posts.html', posts=posts, user=user)

@app.route("/home")
def home():
	print('home route clicked')
	#HnItemDao.flushTable()
	test = HnScraper.getHnItems(3)
	test = [x for x in test if db.session.query(HnItem.id).filter_by(id=x.id).scalar() is None]
	HnItemDao.insertHnItems(test)
	tests = HnItem.query.order_by(HnItem.postedHoursBefore)
	print(len(tests.all()))
	for x in tests:
		print(x)
	#tests = Test.query.order_by(Test.date_posted.desc())
	return render_template('allnews.html', tests=tests)

@app.route("/bookmark")
def bookmark():
	tests = db.session.query(HnItem).join(Bookmarks).filter(Bookmarks.user_id == current_user.id).filter(HnItem.id == Bookmarks.news_id).all()
	return render_template('allnews.html', tests=tests)



@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username = form.username.data, email = form.email.data, password = hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your Account has been created ! You should be able to Login', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)



@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return render_template('quiz2Exp.html', title='Register')
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Login Unsuccessful, Check email and password', 'danger')

	return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
	logout_user()
	return render_template('home.html')

@app.route("/bookmarkNews/<int:news_id>",  methods=['GET', 'POST'])
@login_required
def bookmarkNews(news_id):
	if not current_user.is_authenticated:
		return redirect(url_for('login'))
	bookmark = Bookmarks(current_user.id, news_id)
	db.session.add(bookmark)
	db.session.commit()
	return redirect(url_for('home'))