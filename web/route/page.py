from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from login import login_required, login_user, logout_user, allow_register, getSessionUsername
from extensions import query, html_escape
from flask_wtf import RecaptchaField
from passlib.hash import pbkdf2_sha256
import reg

app = Blueprint('Page', __name__)

class RegistrationForm(Form):
	username = StringField('username', [validators.Length(min=4, max=25)])
	email = StringField('email', [validators.Email(message=('Not a valid email address.')),
		validators.DataRequired()])
	password = PasswordField('password', [
		validators.DataRequired(),
		validators.EqualTo('confirm_password', message='Passwords must match'),
		validators.Length(min=6)
	])
	confirm_password = PasswordField('confirm_password')
	recaptcha = RecaptchaField()

class LoginForm(Form):
	username = StringField('username', [validators.Length(min=4, max=25)])
	password = PasswordField('password', [
		validators.DataRequired(),
		validators.Length(min=6)
	])
	recaptcha = RecaptchaField()

class PassResetForm(Form):
	password = PasswordField('password', [
		validators.DataRequired(),
		validators.Length(min=6)
	])
	new_password = PasswordField('new_password', [
		validators.DataRequired(),
		validators.EqualTo('conf_new_password', message='Passwords must match'),
		validators.Length(min=6)
	])
	conf_new_password = PasswordField('conf_new_password')



@app.route("/login",methods=['GET','POST'])
def login():
	form = LoginForm(request.form)
	if request.method == 'POST' and form.validate():
		user = query.get_userLogin(form.username.data)
		try:
			if not user or not pbkdf2_sha256.verify(form.password.data, user["password"]):
				flash('Please check your login credentials and try again.')
				return redirect(url_for('Page.login'))
			if int(user["is_active"]) == 0:
				flash('Please active your user first.')
				return redirect(url_for('Page.login'))
		except:
			flash('Please check your login credentials and try again.')
			return redirect(url_for('Page.login'))
		login_user(user)
		return redirect(url_for('Page.graph_view'))
	return render_template("login.html",form=form,is_register=current_app.config["ALLOW_REGISTER"])

@app.route("/register",methods=['GET','POST'])
@allow_register
def register():
	form = RegistrationForm(request.form)
	if request.method == 'POST' and form.validate() and not query.get_userLogin(form.username.data) and not query.get_userLogin(form.email.data):
		username = html_escape(form.username.data)
		email = html_escape(form.email.data)
		password = pbkdf2_sha256.using(rounds=10000, salt_size=16).hash(html_escape(form.password.data))
		query.register_user(username, email, password)
		return redirect(url_for('Page.login'))
	return render_template("register.html",form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('Page.login'))

@app.route("/reset",methods=['GET','POST'])
@login_required
def reset():
	form = PassResetForm(request.form)
	if request.method == 'POST' and form.validate():
		username = getSessionUsername()
		user = query.get_userLogin(username)
		try:
			if user and pbkdf2_sha256.verify(form.password.data, user["password"]) and user["is_active"] == 1:
				new_password = pbkdf2_sha256.using(rounds=10000, salt_size=16).hash(html_escape(form.new_password.data))
				query.Updatepassword(username,new_password)
				flash('Your password has been change.')
			else:
				flash('Please check your password and try again.')
		except:
			flash('Please check your password and try again.')
	return render_template("password_reset.html",form=form)  

@app.route("/graph_view")
@login_required
def graph_view():
	return render_template("graph_view.html")
    
@app.route("/graph_view_tradingview")
def graph_view_tradingview():
	return render_template("graph_view_tradingview.html")

@app.route("/logs")
@login_required
def logs():
	return render_template("logs.html")

@app.route("/settings")
@login_required
def settings():
	return render_template("notification - setting.html")

@app.route("/sensor_add")
@login_required
def sensor_add():
	return render_template("sensor_add.html")

@app.route("/conditions")
@login_required
def conditions():
	_type = query.getAllType()
	return render_template("sensor_condition.html",_type=_type)

@app.route("/sensor_view")
@login_required
def sensor_view():
	_type = query.getAllType()
	return render_template("sensor_view.html",_type=_type)    
    
@app.route("/room_add")
@login_required
def room_add():
	reg_building = reg.getAllBuilding()
	return render_template("room_add.html",building=reg_building)

@app.route("/user")
@login_required
def user_manage():
	user = query.getAllUser()
	return render_template("user_manage.html",user=user)
