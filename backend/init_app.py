from app import create_app, hash_password
from backend.models import db, userdatastore
app, api_handler = create_app()



with app.app_context():
    db.create_all()
    print("created db")

    userdatastore.find_or_create_role(name = 'admin', description = 'SuperUser of the application')
    userdatastore.find_or_create_role(name = 'customer', description = 'Customer of the application')
    userdatastore.find_or_create_role(name = 'service_professional', description = 'Service provider of the application')

    if(not userdatastore.find_user(email = 'admin123@gmail.com')):
        userdatastore.create_user(email = 'admin123@gmail.com', password = hash_password('pass'), roles = ['admin'])
    
    if(not userdatastore.find_user(email = 'customer123@gmail.com')):
        userdatastore.create_user(email = 'customer123@gmail.com', password =  hash_password('pass'), roles = ['customer'])
    
    if(not userdatastore.find_user(email = 'service123@gmail.com')):
        userdatastore.create_user(email = 'service123@gmail.com', password =  hash_password('pass'), roles = ['service_professional'])

    db.session.commit()