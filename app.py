from flask import Flask, render_template, flash, jsonify, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, UserMixin, logout_user
from flask_bcrypt import Bcrypt
import os


user = os.environ.get('MYSQL_USER')
psw = os.environ.get('MYSQL_PASSWORD')
host = os.environ.get('MYSQL_SERVICE_HOST') # get it from openshift mysql pod
db = os.environ.get('MYSQL_DATABASE')


# Create app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:merlino@localhost:4000/flask_mysql'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{psw}@{host}/{db}'
app.config['SECURITY_PASSWORD_SALT'] = 'very secret salt'
app.config['SECURITY_LOGIN_USER_TEMPLATE'] = 'login.html'
login_manager = LoginManager(app)
login_manager.login_view = 'login1'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


bcrypt = Bcrypt(app)

# Create database connection object
db = SQLAlchemy(app)

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


@app.route('/login1', methods=['POST', 'GET'])
def login1():
    if request.method == "POST":

        print("richiesta di login POST")

        email = request.form.get('email')
        pswd = request.form.get('pswd')

        user = User.query.filter_by(email=email).first()

        print(user)
        print(user.password)
        print(bcrypt.check_password_hash(user.password, pswd))

        if user and bcrypt.check_password_hash(user.password, pswd):
            login_user(user)

            flash(f'You logged in as {user.email}!', 'success')

            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login failed!', 'warning')

    return render_template('login.html', title='Login')


# Views
@app.route('/')
@app.route('/home')
@login_required
def home():
    return render_template('index.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out!', 'warning')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
