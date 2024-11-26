from flask_restful import Resource
from flask import jsonify, request, make_response
from flask_security import roles_accepted, current_user, auth_required
from backend.models import *



# class AdminSearch(Resource):
#     @roles_accepted('admin')
#     def get(self,query):
#         # formatted_query = query.replace(" ", "").lower()
#         search = "%{}%".format(query)
#         if search:
#             print(search)
#             # services = Service.query.filter(Service.name.like(search)).all()
#             users = User.query.filter(User.fullname.like(search), User.roles.any(name='service_professional')).all()

#             searched_user=[]

#             # for service in services:
#             #     d={
#             #         "sid":service.id,
#             #         "sname":service.name,
#             #     }
#             #     service.append(d)

#             for user in users:
#                 d={
#                     "id": user.id,
#                     "name":user.fullname,
#                     "service_type" : user.service_type 
#                 }
#                 searched_user.append(d)
#                 return make_response(jsonify({"user":searched_user}),200)
#             return make_response(jsonify({"user":[]}),200)
    
     

        # sections = Section.query.filter(Section.section_name.like(search)).all()
        # books = Book.query.filter(Book.title.like(search) | Book.author.like(search)).all()
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
            


