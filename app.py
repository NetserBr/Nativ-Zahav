from turtle import distance
from flask import Flask, jsonify, request, render_template, url_for, redirect
from flask import Response
import os
from PhysicsCalculator import physicsCalculator
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt


# Flask app initialization
app = Flask(__name__, template_folder='templates')

# Data Base initialization
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# Left to choose secrete key
app.config['SECRET_KEY'] = 'thisisasecretkey'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.route('/')
def home():

    # Rendering index html page
    return render_template('home.html')

# Find user from DB


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Define users table


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

# Create Login Form


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=0, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=0, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

# Create Register Form


class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    # Checks if user exist in DB
    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


@app.route('/index', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            # Function for submit button
            # Retrieving data from the html form
            try:
                inptAngle = float(request.form.get('inptAngle'))
                inptInitVel = float(request.form.get('inptInitVel'))
                height = float(request.form.get('height'))

            # Return Bad Request code 400 in case that something
            # failed in the process of converting the inputs to float
            except:
                return Response(
                    "Bad Request: Unexpected calculation request",
                    status=400,
                )

            # Calling the calculator to compute the results
            result = physicsCalculator(inptAngle, inptInitVel, height)

            # Rendering result html poge with the data
            # Loading the correct picture according to the results
            if(float(result['distance']) < 0):
                return render_template("result.html", data=result, visibility1="hidden", visibility2="visible", visibility3="hidden")
            elif(float(result['distance']) == 0.0):
                return render_template("result.html", data=result, visibility1="hidden", visibility2="hidden", visibility3="visible")
            else:
                return render_template("result.html", data=result, visibility1="visible", visibility2="hidden", visibility3="hidden")

    elif request.method == 'GET':
        return render_template('index.html')

# Login page


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Create new form
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            # Compare passwords to check if they are equals
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('index'))

    return render_template('login.html', form=form)

# Register Page


@ app.route('/register', methods=['GET', 'POST'])
def register():
    # Create new form
    form = RegisterForm()

    if form.validate_on_submit():
        # Creating hashed password for better security
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)
