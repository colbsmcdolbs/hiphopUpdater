from flask import render_template, flash, redirect, url_for
from app import db
from app.forms import UnsubForm, SignUpForm
from app.models import User, delete_user, import_user
from app.main import bp


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Home')


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        rappers = form.rappers.data
        email = form.email.data
        for r in rappers:
            import_user(email, r.id)
        return redirect(url_for('success'))
    return render_template('signup.html', title='Sign Up', form=form)


@bp.route('/unsub', methods=['GET', 'POST'])
def unsub():
    form = UnsubForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('That email is not contained in our records.')
            return redirect(url_for('unsub'))
        delete_user(form.email.data)
        return redirect(url_for('success'))
    return render_template('unsub.html', title='Unsubscribe', form=form)


@bp.route('/success')
def unsubsuccess():
    return render_template('success.html', title='Success!')
