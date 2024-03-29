from flask import redirect, render_template, request, url_for

from app import app
from constants import FAILURE_STATUS, SUCCESS_STATUS
from models import LoginActivity, User
from utils import (
    get_previous_login_attempts, check_if_ip_can_login, handle_failed_login)
from validators import validate_password


@app.route('/login', methods=['GET', 'POST'])
def render_login_page():
    if request.method == 'GET':
        request_args = request.args
        if not check_if_ip_can_login(request.remote_addr):
            return redirect('/login-restriction')

        return render_template(
            'login.html', message=request_args.get('message'))

    elif request.method == 'POST':
        form_data = request.form
        ip_address = request.remote_addr

        status = SUCCESS_STATUS

        email = form_data['email']
        password = form_data['password']

        user = User.find_one({'email': email})

        if user is None:
            return render_template(
                'login.html',
                message='Email does not exist')

        if not user.verify_password(password):
            status = FAILURE_STATUS

            handle_failed_login(email, ip_address)

            login_activity = LoginActivity(
                email=email, ip_address=ip_address, status=status
            )
            login_activity.save()

            return redirect(
                url_for('render_login_page',
                        message='Invalid login credentials')
            )

        login_activity = LoginActivity(
            email=email, ip_address=ip_address, status=status
        )
        login_activity.save()

        return redirect('/success')


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

        return redirect(url_for('render_success_page'))


@app.route('/success')
def render_success_page():
    return render_template('success.html')


@app.route('/login-restriction')
def render_login_restriction_page():
    request_ip = request.remote_addr
    previous_attempts = get_previous_login_attempts(request_ip)

    records = previous_attempts['records']

    return render_template(
        'login_restriction.html',
        last_login_time=records[0]['created_at'].isoformat(),
        rest_period=app.config['LOGIN_REST_PERIOD_MINUTES']
    )
