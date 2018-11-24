from datetime import datetime, timedelta
from app import app, db
from models import User, Client, ProductCategory

import click

@app.cli.command('seed')
def seed_db():
    print('Starting seeding the database ...')
    try:
        seed_clients_data()
        seed_product_categories_data()
    except Exception as e:
        print(f'Something went wrong: {e}')
        exit(1)
    
    print('Data successfully seeded!')

def seed_clients_data():
    try:
        # Delete existing data
        db.session.query(Client).delete()
        db.session.commit()
        
        clients = [ 'Client A', 'Client B', 'Client C' ]
        
        for client in clients:
                db.session.add( Client(client) )

        db.session.commit()

    except Exception as e:
        print( f'Error: {e}' )
        db.session.rollback()
        exit(1)

def seed_product_categories_data():
    try:
        # Delete existing data
        db.session.query(ProductCategory).delete()
        db.session.commit()
        
        categories = [ 'Policies', 'Billing', 'Claims', 'Reports' ]
        
        for category in categories:
                db.session.add( ProductCategory(category) )

        db.session.commit()

    except Exception as e:
        print( f'Error: {e}' )
        db.session.rollback()
        exit(1)

if __name__ == '__main__':
    seed_db()