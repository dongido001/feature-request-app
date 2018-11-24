from flask import Flask, request, jsonify, render_template, url_for, session
from app import app, db
from models import Request, Client, ProductCategory
import os
import pprint
from datetime import date

APP_URL = os.getenv("APP_URL", "htttp://localhost:5000/")

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

@app.route('/')
@app.route('/add_request', methods=["POST", "GET"])
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
            'index.html', message=message,
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
def view_requests():
    requests = Request.query.add_columns(Request.id, Request.target_date, Request.title) \
                            .join(Client, Client.id==Request.client_id)  \
                                    .add_columns(Client.name.label('client_name')) \
                            .join(ProductCategory, ProductCategory.id==Request.category_id) \
                                    .add_columns(ProductCategory.name.label('product_category')) \
                            .all()

    return render_template('requests.html', requests=requests)