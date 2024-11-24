from flask_restful import Resource
from flask import jsonify, request, make_response
from flask_security import roles_accepted, current_user, auth_required
from backend.models import *

class AdminSearch(Resource):
    @roles_accepted('admin')
    def get(self):
        data = request.get_json()
        # search_word = data.get("search_word", None)
        search_word = request.args.get("search_word")

        if not search_word:
            return {"message": "Search word is required"}, 400

        professionals = User.query.filter(User.service_type.like(f'%{search_word}%')).all()
        result = []
        for professional in professionals:
            data = {
                'id': professional.id,
                'name': professional.fullname,
                'email': professional.email,
                'service_type': professional.service_type,
                'experience': professional.experience
            }
            result.append(data)
        print(result)
        if result == []:
            return make_response(jsonify({"message": "No Professional found"}), 404)
        return make_response(jsonify({"message": "get all professionals", "result": result}), 200)
            


