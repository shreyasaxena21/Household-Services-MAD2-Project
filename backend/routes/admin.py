from flask_restful import Resource
from flask import jsonify, request, make_response
from flask_security import roles_accepted, current_user, auth_required
from backend.models import *

from matplotlib import pyplot as plt
import matplotlib
matplotlib.use("Agg")
import os


class AdminSearch(Resource):
    @roles_accepted('admin')
    def get(self,query):
        formatted_query = query.replace(" ", "").lower()
        if (formatted_query is not None) and (formatted_query!="") and (formatted_query!=" "): 
            print(query)
            services = db.session.query(Service).filter(Service.name.ilike(f'%{formatted_query}%')).all()
            users = db.session.query(User).filter(User.fullname.ilike(f'%{formatted_query}%'), User.roles.any(name='service_professional')).all()

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
        # data = request.get_json()
        # # search_word = data.get("search_word", None)
        # search_word = request.args.get("search_word")

        # if not search_word:
        #     return {"message": "Search word is required"}, 400

        # professionals = User.query.filter(User.service_type.like(f'%{search_word}%')).all()
        # result = []
        # for professional in professionals:
        #     data = {
        #         'id': professional.id,
        #         'name': professional.fullname,
        #         'email': professional.email,
        #         'service_type': professional.service_type,
        #         'experience': professional.experience
        #     }
        #     result.append(data)
        # print(result)
        # if result == []:
        #     return make_response(jsonify({"message": "No Professional found"}), 404)
        # return make_response(jsonify({"message": "get all professionals", "result": result}), 200)
            


class Adminstats(Resource):
    def get(self):
        service_requests = ServiceRequest.query.all()
        types = []
        for requests in service_requests:
            types.append(requests.service_status)
        plt.clf()
        plt.title("Service Requests")
        plt.xlabel("Service Status")
        plt.ylabel("Number of Service Requests")
        plt.hist(types, color="orange")
        plt.savefig('instance/stats/hist.png')

        # totalservices = db.session.query(Service).count()
        # totalrequests = db.session.query(ServiceRequest).count()
        # totalusers = db.session.query(User).count()

        # services = db.session.query(Service).all()
        # user = db.session.query(User).all()
        # requests = db.session.query(ServiceRequest).all()

        # types = {}
        # for service in services:
        #     if service.name in types:
        #         types[service.name] += 1
        #     else:
        #         types[service.name] = 1

        #     plt.figure(figsize=(10, 6))
        #     plt.pie(types.values(), labels=types.keys(), autopct='%1.1f%%', startangle=140)
        #     plt.title('Number of Services')
        #     filename = 'piechart.png'
        #     filepath = os.path.join('instance/stats', filename)
        #     plt.savefig(filepath)
        #     plt.close()

        
        # Create the response
        # response = {
        #     "totalservices": totalservices,
        #     "totalrequests": totalrequests,
        #     "totalusers": totalusers,
        # }



    # def save_charts():

    #     directory = './instance/stats_images'
    #     if not os.path.exists(directory):
    #         os.makedirs(directory)
    #     # Data extraction for charts
        

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