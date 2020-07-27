from dotenv import load_dotenv
from flask import Flask, flash, render_template, request, url_for, redirect, jsonify, session
from models.models import Db, User, Post
from forms.forms import SignupForm, LoginForm, NewpostForm
from os import environ
from passlib.hash import sha256_crypt

load_dotenv('.env')

################################################ # Flask migrate commands after pip3 install migrate ######### # 1) flask db init # 2) flask db migrate -m "first migration" # 3) flask db upgrade # to push migrations # 4) python3 app.py ##############################################
#date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/lab5b'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = environ.get('SECRET_KEY')
Db.init_app(app)


#GET /
@app.route('/')
@app.route('/index')
def index():
    # Control by login status
    if 'username' in session:
        session_user = User.query.filter_by(username=session['username']).first()
        posts = Post.query.filter_by(author=session_user.uid).all()
        return render_template('index.html', title='Home', posts=posts, session_username=session_user.username)
    else:
        all_posts = Post.query.all()
        return render_template('index.html', title='Home', posts=all_posts)


#GET & POST /login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Init form
    form = LoginForm()
    # If post
    if request.method == 'POST':
        # Init credentials from form request
        username = request.form['username']
        password = request.form['password']

        # Init user by Db query
        user = User.query.filter_by(username=username).first()

        # Control login validity
        if user is None or not sha256_crypt.verify(password, user.password):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        else:
            session['username'] = username
            return redirect(url_for('index'))

    # If GET
    else:
        return render_template('login.html', title='Login', form=form)


# POST /logout
@app.route('/logout', methods=['POST'])
def logout():
    # Logout
    session.clear()
    return redirect(url_for('index'))


# GET & POST /newpost
@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    # Init form
    form = NewpostForm()

    # If POST
    if request.method == 'POST':
        # Init user from poster
        session_user = User.query.filter_by(username=session['username']).first()
        # Init content from form request
        content = request.form['content']
        # Create in DB
        new_post = Post(author=session_user.uid, content=content)
        Db.session.add(new_post)
        Db.session.commit()

        return redirect(url_for('index'))

     # If GET
    else:
        return render_template('newpost.html', title='Newpost', form=form)


# GET & POST /signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Init form
    form = SignupForm()

    # IF POST
    if request.method == 'POST':

        # Init credentials from form request
        username = request.form['username']
        password = request.form['password']

        # Init user from Db query
        existing_user = User.query.filter_by(username=username).first()

        # Control new credentials
        if existing_user:
            flash('The username already exists. Please pick another one.')
            return redirect(url_for('signup'))
        else:
            user = User(username=username, password=sha256_crypt.hash(password))
            Db.session.add(user)
            Db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))

    # IF POST
    else:
        return render_template('signup.html', title='Signup', form=form)
