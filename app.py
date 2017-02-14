from flask import Flask, render_template, url_for, redirect, request
from models import *
from utils import *
from termcolor import colored
from config import *

app = Flask(__name__)

@app.before_request
def before_request():
	initialize()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
	username = request.form['username']
	email = request.form['email']
	password = request.form['password']
	confirm_password = request.form['confirm-password']
	
	if username and email and password:
		if password == confirm_password:
			try:
				User.select().where(User.username == username).get().username
				return render_template('login.html', nomatch=True, message=user_exists)
			except:
				User.create(username=username, email=email, password=computeMD5hash(password))
				return redirect(url_for('projects'))
		else:
			return render_template('login.html', nomatch=True, message=password_no_match)

@app.route('/lgn', methods=['POST'])
def lgn():
	username = request.form['username']
	password = request.form['password']

	try:
		truepass = User.select().where(User.username == username).get().password
	except:
		return render_template('login.html', invalid=True)
	if password and truepass == computeMD5hash(password):
		# return redirect(url_for('projects'))
		try:
			proj = []
			for i in Project.select():
				if i.username == username:
					proj.append({'project_name':i.project_name})
					proj.append({'progress':i.progress})

			# proj = Project.select().where(Project.username == username).get()
			print(colored(proj, 'red'))
		except:
			proj = 0
		return render_template('projects.html', proj=proj)
	else:
		return render_template('login.html', invalid=True)


@app.route('/projects')
def projects():
	return render_template('projects.html')


@app.teardown_request
def teardown_request(request):
	db.close()


if __name__ == '__main__':
	app.run(debug=True)
