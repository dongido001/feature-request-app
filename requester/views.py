from flask import Flask, Blueprint, request, jsonify, render_template, url_for, session, flash, redirect
from requester import create_app, db
from requester.models import User, Request, Client, ProductCategory
import os
import pprint
from datetime import datetime
from flask_login import login_user, login_required, logout_user

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/add_request', methods=["POST", "GET"])
@login_required
def add_request():
    clients = Client.query.all()
    product_categories = ProductCategory.query.all()

    if request.method != "POST":
        return render_template(
            'index.html',
            product_categories=product_categories,
            clients=clients
        )
    
    # Go ahead and respond to the POST request
    title = request.form.get("title")
    description = request.form.get("description")
    client_id = request.form.get("client")
    priority = request.form.get("priority")
    target_date = datetime.strptime(request.form.get("target_date"), "%Y-%m-%d").date()
    product_area = request.form.get("product_area")

    if not (title and description and client_id and priority and target_date and product_area):
        message = {
            'message': "All fields are required",
            'error': True
        }
        return render_template(
            'index.html', 
            message=message,
            product_categories=product_categories,
            clients=clients
        )

    try:
        new_request = Request()
        new_request.title = title
        new_request.description = description
        new_request.client_id = client_id
        new_request.priority = priority
        new_request.target_date = target_date
        new_request.category_id = product_area
        db.session.add(new_request)
        db.session.commit()
    except:
        message = {
            'message': f"An error occured: Database error",
            'error':  True
        }
        return render_template(
            'index.html', 
            message=message,
            product_categories=product_categories,
            clients=clients
        )

    message = {
        'message': "Request added",
        'error':  False
    }

    return render_template(
        'index.html',
        message=message,
        product_categories=product_categories,
        clients=clients
    )

@bp.route('/requests')
@login_required
def view_requests():
    requests = Request.query.add_columns(Request.id, Request.target_date, Request.title, Request.priority) \
                            .join(Client, Client.id==Request.client_id)  \
                                    .add_columns(Client.name.label('client_name')) \
                            .join(ProductCategory, ProductCategory.id==Request.category_id) \
                                    .add_columns(ProductCategory.name.label('product_category')) \
                            .all()

    return render_template('requests.html', requests=requests)


@bp.route('/login', methods=["POST", "GET"])
def login():
    if request.method != "POST":
        return render_template('auth/login.html')

    username = request.form.get('username')
    password = request.form.get('password')

    if not (username and password):
        message = {
            'message': "All fields are required",
            'error': True
        }
        return render_template(
            'index.html', 
            message=message
        )

    _user = User.query.filter_by(username=username).first()

    if not ( _user and _user.check_password_hash(password) ):
        message = {
            'message': "Login failed. Try again.",
            'error': True
        }
        return render_template('auth/login.html', message=message)

    login_user(_user)
    session['logged_in'] = True
    return redirect(url_for('main.view_requests'))


@bp.route("/logout", methods=["GET"])
def logout():
    logout_user()
    session['logged_in'] = False
    return render_template("auth/login.html")


@bp.route("/get_clients")
def get_clients():
    clients = Client.query.all()

    response = {
        'status': 'success',
        'data': [ 
            {'client_id': client.id, 'client_name': client.name} 
            for client in clients
        ]
    }
    return jsonify(response)

@bp.route("/get_client_priority/<int:client_id>")
def get_client_priority(client_id):
    requests = Request \
                .query.filter(Request.client_id==client_id) \
                .add_columns(Request.priority) \
                .all()
                
    priorities = [request.priority for request in requests]

    generate_priority = [
        priority 
        for priority in range(1, (10 + len(priorities) + 1) )
        if priority not in priorities
    ]

    response = {
        'priorities': generate_priority
    }

    return jsonify(response)