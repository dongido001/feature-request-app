from flask import Flask, request, jsonify, render_template, url_for, session, flash, redirect
from app import app, db
from models import User, Request, Client, ProductCategory
import os
import pprint
from datetime import date
from flask_login import LoginManager, login_user, login_required, logout_user

login_manager = LoginManager()
login_manager.init_app(app)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    message = {
        'message': "You need to login",
        'error': True
    }
    return render_template('auth/login.html', message=message)

@app.route('/')
@app.route('/add_request', methods=["POST", "GET"])
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
    target_date = date.fromisoformat(request.form.get("target_date"))
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

@app.route('/requests')
@login_required
def view_requests():
    requests = Request.query.add_columns(Request.id, Request.target_date, Request.title) \
                            .join(Client, Client.id==Request.client_id)  \
                                    .add_columns(Client.name.label('client_name')) \
                            .join(ProductCategory, ProductCategory.id==Request.category_id) \
                                    .add_columns(ProductCategory.name.label('product_category')) \
                            .all()

    return render_template('requests.html', requests=requests)


@app.route('/login', methods=["POST", "GET"])
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

    registered_user = User.query.filter_by(username=username,password=password).first()
    if registered_user is None:
        message = {
            'message': "Login failed. Try again.",
            'error': True
        }
        return render_template('auth/login.html', message=message)

    login_user(registered_user)
    session['logged_in'] = True
    return redirect(url_for('view_requests'))


@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    session['logged_in'] = False
    return render_template("auth/login.html")