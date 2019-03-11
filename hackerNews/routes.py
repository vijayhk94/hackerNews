import os
import secrets
from flask import render_template, url_for, flash, redirect,request
from hackerNews import app, db, bcrypt
from hackerNews.forms import RegistrationForm, LoginForm
from hackerNews.models import User, HnItem, Bookmarks, DeletedItems, ReadItems
from hackerNews.HnScraper import HnScraper
from hackerNews.HnItemDao import HnItemDao
from flask_login import login_user, current_user, logout_user, login_required
import re		

@app.route("/")
def main():
	return render_template('allnews.html')

@app.route("/home")
def home():
	if not current_user.is_authenticated:
		return render_template('allnews.html')
	news = HnItem.query.order_by(HnItem.postedHoursBefore)
	deletedItems = db.session.query(HnItem).join(DeletedItems).filter(DeletedItems.user_id == current_user.id).filter(HnItem.id == DeletedItems.news_id)
	if deletedItems is not None:
		deletedItemsList = deletedItems.all()
		news = [x for x in news if x not in deletedItemsList]	
	return render_template('allnews.html', tests=news[:90])

@app.route("/refresh")
def refresh():
	if not current_user.is_authenticated:
		return render_template('allnews.html')
	news = HnScraper.getHnItems(3)
	news = [x for x in news if db.session.query(HnItem.id).filter_by(id=x.id).scalar() is None]
	HnItemDao.insertHnItems(news)
	return redirect(url_for('home'))

@app.route("/bookmarks")
def bookmarks():
	if not current_user.is_authenticated:
		return render_template('allnews.html')
	bookmarkedItems = db.session.query(HnItem).join(Bookmarks).filter(Bookmarks.user_id == current_user.id).filter(HnItem.id == Bookmarks.news_id)
	bookmarkedItemsList = []
	if bookmarkedItems is not None:
		bookmarkedItemsList = bookmarkedItems.all()
	return render_template('allnews.html', tests=bookmarkedItemsList)



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

@app.route("/unBookmarkNews/<int:news_id>",  methods=['GET', 'POST'])
@login_required
def unBookmarkNews(news_id):
	if not current_user.is_authenticated:
		return redirect(url_for('login'))
	db.session.query(Bookmarks).filter_by(user_id = current_user.id, news_id = news_id).delete()
	db.session.commit()
	return redirect(url_for('home'))


@app.route("/deleteNews/<int:news_id>",  methods=['GET', 'POST'])
@login_required
def deleteNews(news_id):
	if not current_user.is_authenticated:
		return redirect(url_for('login'))
	deletedItem = DeletedItems(current_user.id, news_id)
	db.session.add(deletedItem)
	db.session.commit()
	return redirect(url_for('home'))

@app.route("/markAsRead/<int:news_id>",  methods=['GET', 'POST'])
@login_required
def markAsRead(news_id):
	if not current_user.is_authenticated:
		return redirect(url_for('login'))
	readItem = ReadItems(current_user.id, news_id)
	db.session.add(readItem)
	db.session.commit()
	return redirect(url_for('home'))

@app.route("/unMarkAsRead/<int:news_id_>",  methods=['GET', 'POST'])
@login_required
def unMarkAsRead(news_id_):
	if not current_user.is_authenticated:
		return redirect(url_for('login'))
	db.session.query(ReadItems).filter_by(user_id = current_user.id, news_id = news_id_).delete()
	db.session.commit()
	return redirect(url_for('home'))