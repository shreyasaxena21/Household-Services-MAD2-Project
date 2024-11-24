from flask import Flask, jsonify, request
from backend.config import LocalDevelopmentConfig
from backend.models import userdatastore, db, Service, User, ServiceRequest
from app_security import security, hash_password
from flask_security import verify_password, roles_accepted
from flask_restful import Api
from flask_cors import CORS
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use("Agg")

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


from backend.routes.admin import AdminSearch
api_handler.add_resource(AdminSearch, '/api/adminsearch')


from backend.routes.service_request import CreateServiceRequest, SpecificServiceRequest, CloseServiceRequest, GetCompletedRequests, GetCustomerRequests, AcceptRequest, GetServiceRequest, RejectRequest
api_handler.add_resource(CreateServiceRequest, '/api/createservicerequest')
api_handler.add_resource(SpecificServiceRequest, '/api/servicerequest/<int:id>')
api_handler.add_resource(CloseServiceRequest, '/api/closeservicerequest/<int:id>')
api_handler.add_resource(GetCompletedRequests, '/api/completedservicerequest')
api_handler.add_resource(GetCustomerRequests, '/api/customerrequest/<int:id>')
api_handler.add_resource(AcceptRequest, '/api/acceptrequest/<int:id>')
api_handler.add_resource(RejectRequest, '/api/rejectrequest/<int:id>')
api_handler.add_resource(GetServiceRequest, '/api/getservicerequest/<int:id>')


from backend.routes.celery_routes import DailyMail, MonthlyREport, ExportCSV
api_handler.add_resource(DailyMail, '/api/celery/dailyremainder')
api_handler.add_resource(MonthlyREport, '/api/celery/monthlyreport')
api_handler.add_resource(ExportCSV, '/api/celery/createcsv')


#--------------------------------------------------------Stats----------------------------------------------------------------

@app.route('/showstats')
def stats():
    # Count total services, service requests, and users
    totalservices = db.session.query(Service).count()
    totalrequests = db.session.query(ServiceRequest).count()
    totalusers = db.session.query(User).count()

    # Save plots
    save_charts()

    # Create the response
    response = {
        "totalservices": totalservices,
        "totalrequests": totalrequests,
        "totalusers": totalusers,
    }

    return jsonify(response), 200

def save_charts():
    # Data extraction for charts
    services = db.session.query(Service).all()
    user = db.session.query(User).all()
    requests = db.session.query(ServiceRequest).all()

    types = {}
    for service in services:
        if service.name in types:
            types[service.name] += 1
        else:
            types[service.name] = 1

        plt.figure(figsize=(10, 6))
        plt.pie(types.values(), labels=types.keys(), autopct='%1.1f%%', startangle=140)
        plt.title('Number of Services')
        plt.savefig('./instance/stats_images/piechart.png')
        plt.close()

        # 2. Line Graph: User Book Request Behavior
    #     data = {'date': [], 'requests': []}
    #     for req in requests:
    #         data['date'].append(req.adate)
    #         data['requests'].append(req.status)

    #     df = pd.DataFrame(data)
    #     df['date'] = pd.to_datetime(df['date'])
    #     df = df.groupby('date').size()

    #     plt.figure(figsize=(12, 6))
    #     plt.plot(df.index, df.values, marker='o', linestyle='-')
    #     plt.xlabel('Date')
    #     plt.ylabel('Number of Requests')
    #     plt.title('User Book Request Behavior Over Time')
    #     plt.grid(True)
    #     plt.savefig('../frontend/vue-project/src/assets/behaviour.png')
    #     plt.close()

    # # 3. Histogram: Book Requests
    #     status_counts = [req.status for req in requests]

    #     if status_counts:
    #         plt.figure(figsize=(10, 6))
    #         plt.hist(status_counts, bins=range(4), edgecolor='black')
    #         plt.xlabel('Request Status')
    #         plt.ylabel('Frequency')
    #         plt.title('Histogram of Book Requests')
    #         plt.xticks([0, 1, 2], ['Rejected', 'Pending', 'Accepted'])
    #         plt.grid(True)
    #         plt.savefig('../frontend/vue-project/src/assets/histo.png')
    #         plt.close()

    # # 4. Bar Chart: Number of Books per Author
    # author_book_count = {}
    # for book in books:
    #     author_book_count[book.author] = author_book_count.get(book.author, 0) + 1
    
    # if author_book_count:

    #     plt.figure(figsize=(12, 8))
    #     plt.barh(list(author_book_count.keys()), author_book_count.values(), color='skyblue')
    #     plt.xlabel('Number of Books')
    #     plt.title('Number of Books per Author')
    #     plt.gca().invert_yaxis()
    #     plt.grid(axis='x')
    #     plt.savefig('../frontend/vue-project/src/assets/bar.png')
    #     plt.close()


# @app.route('/showadminsstats', methods=['GET'])
# @roles_accepted('admin')
# def show_admin_stats():
#     services = Service.query.all()
#     types = {}
#     for service in services:
#         if service.name in types:
#             types[service.name] += 1
#         else:
#             types[service.name] = 1

#     # Generate pie chart
#     plt.clf()
#     plt.figure(figsize=(10, 6))
#     plt.pie(types.values(), labels=types.keys(), autopct='%1.1f%%', startangle=140)
#     plt.title('Number of Services')
#     plt.savefig('./frontend/src/assets/stats/piechat.png')
#     plt.close()

#     # Generate histogram
#     customer = User.query.filter(User.roles.any(name='customer')).all()
#     professional = User.query.filter(User.roles.any(name='service_professional')).all()
#     types = []
#     for c in customer:
#         types.append(c.type)
#     for p in professional:
#         types.append(p.type)
#     plt.clf()
#     plt.title("Active Users")
#     plt.xlabel("Type of User")
#     plt.ylabel("Number of Users")
#     plt.hist(types, color="maroon")
#     plt.savefig()
#     plt.close()

#     return "Stats generated successfully!"

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