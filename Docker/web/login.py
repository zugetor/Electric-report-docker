from functools import wraps
from flask import session, redirect, url_for, flash
from time import time
from extensions import query

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if 'id' not in session or session['id'] is None:
			flash('Please Login to access this page.')
			return redirect(url_for('Page.login'))
		user = query.get_userByid(session['id'])
		if(user["flogout"] == 1 or user['is_active'] == 0):
			logout_user()
			return redirect(url_for('Page.login'))
		session['login_time'] = int(time())
		return f(*args, **kwargs)
	return decorated_function

def login_user(user):
	session['username'] = user["username"]
	session['id'] = user["id"]
	session['login_time'] = int(time())

def logout_user():
	session.pop('id', None)
	session.pop('username', None)
	session.pop('login_time', None)