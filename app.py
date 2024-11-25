import io
from flask import Flask, Response, jsonify, request, make_response
from backend.config import LocalDevelopmentConfig
from backend.models import userdatastore, db, Service, User, ServiceRequest
from app_security import security, hash_password
from flask_security import verify_password, roles_accepted
from flask_restful import Api
from flask_cors import CORS

from matplotlib import pyplot as plt
import matplotlib
matplotlib.use("Agg")
import os


def make_celery(app):
        from backend import celery_config
        from celery import Celery
        celery = Celery(app.import_name)
        celery.config_from_object(celery_config)
        return celery

def createApp():
    app = Flask(__name__, template_folder="template")
    from backend.caching import cache
    from backend.mailer import mail

    app.config.from_object(LocalDevelopmentConfig)
    
    #model init
    db.init_app(app)


    security.init_app(app, userdatastore, register_blueprint = False)

    api = Api(app)

    CORS(app, supports_credentials=True)

    app.app_context().push()

    cache.init_app(app)

    celery = make_celery(app)
    # app.config.timezone = 'UTC'

    mail.init_app(app)


    return app, api, celery

app, api_handler, celery = createApp()




from celery.schedules import crontab


#-------------------------------------------Celery Beat Scheduling---------------------------------------------------------

celery.conf.beat_schedule = {
    "daily_remainders" : {
        "task" : 'backend.task.daily_remainder',
        #in the evening 7pm
        'schedule' : crontab(minute=00, hour=19)
    },

    "monthly_report" : {
        "task" : 'backend.task.monthly_report',
        #1st of every month at 6 pm
        'schedule' : crontab(minute=00, hour=18, day_of_month=1)
    }
}

from backend import task

@app.route("/triggerexport", methods=["GET"])
@roles_accepted("admin")
def triggerexport():
    task.create_csv.delay()
    return jsonify({"message":"You will get a mail soon!!"}),200


#---------------------------------------Regsitering API Endpoints-----------------------------------------------------------

from backend.routes.auth import Login, Register, Logout, GetUsers, GetProfessionals, ApproveProfessionals, FlagUser, GetActiveProf, GetSpecificCustomer,GetSpecificProfessional, EditCustomerProfile, EditProfessionalProfile, Unblock, Getblockedusers
api_handler.add_resource(Login, '/api/login')
api_handler.add_resource(Register, '/api/register')
api_handler.add_resource(Logout, '/api/logout')
api_handler.add_resource(GetUsers, '/api/getusers')
api_handler.add_resource(GetProfessionals, '/api/getprofessional')
api_handler.add_resource(ApproveProfessionals, '/api/approveprofessional/<int:id>')
api_handler.add_resource(FlagUser, '/api/flaguser/<int:id>')
api_handler.add_resource(Unblock, '/api/unblock/<int:id>')
api_handler.add_resource(GetActiveProf, '/api/getactiveprof')
api_handler.add_resource(GetSpecificCustomer, '/api/getcustomer/<int:id>')
api_handler.add_resource(GetSpecificProfessional, '/api/getprofessional/<int:id>' )
api_handler.add_resource(EditCustomerProfile, '/api/editcustomer/<int:id>')
api_handler.add_resource(EditProfessionalProfile, '/api/editprofessional/<int:id>')
api_handler.add_resource(Getblockedusers, '/api/getblockedusers')



from backend.routes.service import GeneralService, SpecificService
api_handler.add_resource(GeneralService, '/api/service')
api_handler.add_resource(SpecificService, '/api/service/<int:id>')


# from backend.routes.admin import Adminstats
# # api_handler.add_resource(AdminSearch, '/api/adminsearch/<string:query>')
# api_handler.add_resource(Adminstats, '/api/adminstats')


from backend.routes.service_request import CreateServiceRequest, SpecificServiceRequest, CloseServiceRequest, GetCompletedRequests, GetCustomerRequests, AcceptRequest, GetServiceRequest, RejectRequest, GetAcceptedRequests
api_handler.add_resource(CreateServiceRequest, '/api/createservicerequest')
api_handler.add_resource(SpecificServiceRequest, '/api/servicerequest/<int:id>')
api_handler.add_resource(CloseServiceRequest, '/api/closeservicerequest/<int:id>')
api_handler.add_resource(GetCompletedRequests, '/api/completedservicerequest')
api_handler.add_resource(GetCustomerRequests, '/api/customerrequest/<int:id>')
api_handler.add_resource(AcceptRequest, '/api/acceptrequest/<int:id>')
api_handler.add_resource(RejectRequest, '/api/rejectrequest/<int:id>')
api_handler.add_resource(GetServiceRequest, '/api/getservicerequest/<int:id>')
api_handler.add_resource(GetAcceptedRequests, '/api/acceptedrequests/<int:id>')


from backend.routes.celery_routes import DailyMail, MonthlyREport, ExportCSV
api_handler.add_resource(DailyMail, '/api/celery/dailyremainder')
api_handler.add_resource(MonthlyREport, '/api/celery/monthlyreport')
api_handler.add_resource(ExportCSV, '/api/celery/createcsv')

@app.route('/adminsearch/<string:query>', methods=['GET'])
@roles_accepted('admin')
def search(query):
    formatted_query = query.replace(" ", "").lower()
    if formatted_query:
        print(f"Search query: {formatted_query}")
        services = db.session.query(Service).filter(Service.name.ilike(f'%{formatted_query}%')).all()
        users = db.session.query(User).filter(
            User.fullname.ilike(f'%{formatted_query}%'), 
            User.roles.any(name='service_professional')
        ).all()

        service=[]
        user=[]

        for s in services:
            d={
                "sid":s.id,
                "sname":s.name,
            }
            service.append(d)

        for i in users:
            d={
                "uid":i.id,
                "uname":i.fullname
            }
            users.append(d)

        return make_response({"services":service,"user":user}),200
    return make_response({"services":[],"user":[]}),200

#--------------------------------------------------------Stats-------------------------------------------------------------

def create_pie_chart(service_counts):
    """Create and return a pie chart for services."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.pie(
        service_counts.values(),
        labels=service_counts.keys(),
        autopct="%1.1f%%",
        startangle=140,
    )
    ax.set_title("Distribution of Services")

    img_io = io.BytesIO()
    fig.savefig(img_io, format="png")
    img_io.seek(0)  # Rewind to the beginning of the BytesIO object
    plt.close(fig)  # Close the plot to free resources

    return img_io


def save_charts():
    """Fetch service data and generate the pie chart."""
    # Fetch all services from the Service table
    services = db.session.query(Service).all()

    service_counts = {}
    for service in services:
        # Count the occurrence of each service by name
        service_counts[service.name] = service_counts.get(service.name, 0) + 1

    return create_pie_chart(service_counts)

@app.route("/api/showstats", methods=["GET"])
def stats():
    """API endpoint to return the services pie chart."""
    img_io = save_charts()
    return Response(img_io, mimetype="image/png")



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