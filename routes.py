from flask import redirect, render_template, request

from app import app
from constants import FAILURE_STATUS, SUCCESS_STATUS
from models import LoginActivity, User
from utils import get_previous_login_attempt, handle_failed_login
from validators import validate_password


@app.route('/login', methods=['GET', 'POST'])
def render_login_page():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        form_data = request.form
        ip_address = request.remote_addr

        status = SUCCESS_STATUS

        email = form_data['email']
        password = form_data['password']

        user = User.find({'email': email})

        if user is None or user.verify_password(password):
            status = FAILURE_STATUS
            handle_failed_login(email, ip_address)

            return redirect('/login')

        login_activity = LoginActivity(
            email=email, ip_address=ip_address, status=status
        )
        login_activity.save()

        return render_template('success.html')


@app.route('/signup', methods=['GET', 'POST'])
def render_signup_page():
    if request.method == 'GET':
        return render_template('signup.html')

    elif request.method == 'POST':
        form_data = request.form

        fullname = form_data['fullname']
        email = form_data['email']
        password = form_data['password']
        verify_password = form_data['verify_password']

        if password != verify_password:
            return render_template(
                'signup.html', message='Passwords do not match')

        try:
            validate_password(password)
        except ValueError:
            return render_template('signup.html', message='Invalid password')

        user = User(
            fullname=fullname,
            email=email,
            password=password
        )

        user.save()

        return render_template('success.html')
