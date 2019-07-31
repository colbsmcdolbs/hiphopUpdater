from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html', title='Sign Up')


@app.route('/unsub', methods=['GET', 'POST'])
def unsub():
    return render_template('unsub.html', title='Unsubscribe')
