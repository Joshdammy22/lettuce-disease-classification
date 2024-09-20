# app/auth/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from app.models import *
from app.auth.forms import *
from werkzeug.security import generate_password_hash, check_password_hash
from .utils import *
from flask import current_app

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        # Redirect already authenticated users to the dashboard
        return redirect(url_for('main.dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! you can now proceed to login.', 'info')
        return redirect(url_for('auth.login'))  # Redirect to login page after successful registration

    if form.errors:
        for field_errors in form.errors.values():
            for error in field_errors:
                flash(error, 'danger')

    return render_template('register.html', title='Register', form=form)



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            if not user.email_verified:
                flash('Please verify your email address before logging in.', 'warning')
                return redirect(url_for('auth.login'))
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    if form.errors:
        for field_errors in form.errors.values():
            for error in field_errors:
                flash(error, 'danger')
    return render_template('login.html', title='Login', form=form)



@auth.route('/verify_email/<token>', methods=['GET', 'POST'])
def verify_email(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.register'))
    
    # Check if the email is already verified
    if user.email_verified:
        flash('Your email is already verified.', 'info')
        return redirect(url_for('auth.login'))
    
    user.email_verified = True
    user.email_verification_token = None
    db.session.commit()
    
    flash('Your email has been verified! You can now log in.', 'success')
    return redirect(url_for('auth.login'))

@login_required
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('reset_request.html', form=form)



@auth.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

