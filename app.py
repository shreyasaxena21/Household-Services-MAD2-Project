from flask import Flask, jsonify, request
from backend.config import LocalDevelopmentConfig
from backend.models import userdatastore, db, Service
from app_security import security, hash_password
from flask_security import verify_password
from flask_restful import Api
from flask_cors import CORS


def createApp():
    app = Flask(__name__)

    app.config.from_object(LocalDevelopmentConfig)
    
    #model init
    db.init_app(app)


    security.init_app(app, userdatastore, register_blueprint = False)

    api = Api(app)

    CORS(app, supports_credentials=True)

    app.app_context().push()

    return app, api

app, api_handler = createApp()


#-------------------------------Regsitering API Endpoints----------------------------

from backend.routes.auth import Login, Register, Logout, GetUsers, GetProfessionals, ApproveProfessionals, FlagUser, GetActiveProf
api_handler.add_resource(Login, '/api/login')
api_handler.add_resource(Register, '/api/register')
api_handler.add_resource(Logout, '/api/logout')
api_handler.add_resource(GetUsers, '/api/getusers')
api_handler.add_resource(GetProfessionals, '/api/getprofessional')
api_handler.add_resource(ApproveProfessionals, '/api/approveprofessional/<int:id>')
api_handler.add_resource(FlagUser, '/api/flaguser/<int:id>')
api_handler.add_resource(GetActiveProf, '/api/getactiveprof')



from backend.routes.service import GeneralService, SpecificService
api_handler.add_resource(GeneralService, '/api/service')
api_handler.add_resource(SpecificService, '/api/service/<int:id>')


from backend.routes.admin import AdminSearch
api_handler.add_resource(AdminSearch, '/api/adminsearch')
# api_handler.add_resource(toggle_user_status, '/api/toggle_user_status/<int:id>')
# api_handler.add_resource(UserResources, '/api/users', '/api/user/<int:id>')

from backend.routes.service_request import CreateServiceRequest, SpecificServiceRequest, CloseServiceRequest, GetCompletedRequests, GetCustomerRequests, AcceptRequest
api_handler.add_resource(CreateServiceRequest, '/api/createservicerequest')
api_handler.add_resource(SpecificServiceRequest, '/api/servicerequest/<int:id>')
api_handler.add_resource(CloseServiceRequest, '/api/closeservicerequest/<int:id>')
api_handler.add_resource(GetCompletedRequests, '/api/completedservicerequest')
api_handler.add_resource(GetCustomerRequests, '/api/customerrequest/<int:id>')
api_handler.add_resource(AcceptRequest, '/api/acceptrequest/<int:id>')


with app.app_context():
    db.create_all()
    print("created db")

    userdatastore.find_or_create_role(name = 'admin', description = 'SuperUser of the application')
    userdatastore.find_or_create_role(name = 'customer', description = 'Customer of the application')
    userdatastore.find_or_create_role(name = 'service_professional', description = 'Service provider of the application')

    if(not userdatastore.find_user(email = 'admin123@gmail.com')):
        userdatastore.create_user(email = 'admin123@gmail.com', password = hash_password('pass'), roles = ['admin'], is_approved=1, fullname='admin')
    
    if(not userdatastore.find_user(email = 'customer123@gmail.com')):
        userdatastore.create_user(email = 'customer123@gmail.com', password =  hash_password('pass'), roles = ['customer'],is_approved=1, fullname='customer')
    
    if(not userdatastore.find_user(email = 'service123@gmail.com')):
        userdatastore.create_user(email = 'service123@gmail.com', password =  hash_password('pass'), roles = ['service_professional'], fullname='service pro')
    
    db.session.commit()
    

    # Create services only if they don't already exist
    services = [
        {
            "name": "AC Repairing",
            "price": 500,
            "description": "Repairing of AC",
            "time_required": 2,
            "image": "Null",
            "prof_id" : 3
        },
        {
            "name": "Home Cleaning",
            "price": 1500,
            "description": "Cleaning Services",
            "time_required": 4,
            "image": "Null",
            "prof_id" : 3
        },
        {
            "name": "Plumbing Services",
            "price": 900,
            "description": "Plumbing Services",
            "time_required": 5,
            "image": "Null",
            "prof_id" : 3
        },
        {
            "name": "Electrical Services",
            "price": 2500,
            "description": "Electrical Services",
            "time_required": 3,
            "image": "Null",
            "prof_id" : 3
        },
    ]

    for service_data in services:
        existing_service = Service.query.filter_by(name=service_data["name"]).first()
        if not existing_service:
            service = Service(**service_data)
            db.session.add(service)

    db.session.commit()
    print("Created Services")

if (__name__ == '__main__'):
    app.run(port = 5002)