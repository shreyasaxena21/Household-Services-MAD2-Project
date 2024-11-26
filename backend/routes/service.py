from flask_restful import Resource
from flask import jsonify, make_response, request
from flask_security import roles_accepted, current_user
from backend.models import Service, db
import os

#-------------------------------------------------Admin---------------------------------------------------------------------

class GeneralService(Resource):
    @roles_accepted('admin')
    def post(self):
        # data = request.get_json()
        data = request.form

        # Extract data from the request
        name = data.get('name')
        if not name:
            return jsonify({"message": "name is required"})
        
        price = data.get('price')
        if not price:
            return jsonify({"message": "price is required"})
        
        time_required = data.get('time_required')
        if not time_required:
            return jsonify({"message": "time is required"})
        
        description = data.get('description')
        if not description:
            return jsonify({"message": "description is required"})
        
        professional_id = data.get('professional_id')
        
        image = request.files['img']

        search_name = raw(name)
        
        # Check if the user has the admin role
        if current_user.has_role('admin'):
            # Create a new Service object
            service = Service(
                name=name,
                price=price, 
                time_required=time_required, 
                description=description,
                prof_id = professional_id,
                search_name = search_name


            )
       
            # Add the service to the session and commit
            db.session.add(service)
            db.session.commit()
            service_id = service.id
            filename = f"{service_id}.jpg"
            print(filename)
            image_path = os.path.join('instance/serviceimage', filename)
            image.save(image_path)
            
            # Use the service object's id attribute
            return make_response(jsonify({
                "message": "Service created successfully",
                "id": service.id,  # Correctly use the service object's id
                "service name": name
            }), 201)


#----------------------------------------------------Common-----------------------------------------------------------------

    @roles_accepted('admin', 'service_professional', 'customer')
    def get(self):
        service = Service.query.all()
        data = []
        for services in service:
            serv = {
                    'id': services.id,
                    'name': services.name,
                    'description': services.description,
                    'price' : services.price,
                    'time_required' : services.time_required
                }
            data.append(serv)
        print(data)
        if data == []:
            return make_response(jsonify({"message": "No Service found"}), 404)
        return make_response(jsonify({"message": "get all services", "data": data}), 200)

class SpecificService(Resource):

    @roles_accepted('admin', 'service_professional', 'customer')
    def get(self, id):
        services = Service.query.filter_by(id = id).first()
        service = {
                    'id': services.id,
                    'name': services.name,
                    'description': services.description,
                    'price' : services.price,
                    'time_required' : services.time_required
                }
        
        if not service:
            return make_response(jsonify({"message" : "No Service found by that id"}), 404)
        
        return make_response(jsonify({"message" : "get specific service", "data" : service}), 200)
    
    @roles_accepted('admin')
    def put(self, id):
        service = Service.query.filter_by(id = id).first()

        if not service:
            return make_response(jsonify({"message" : "No Service found by that id"}), 404)
        
        data = request.get_json()
        name = data['name']
        if not name:
            return jsonify({"message": "name is required"})
        
        price = data['price']
        if not price:
            return jsonify({"message": "price is required"})
        
        time_required = data['time_required']
        if not time_required:
            return jsonify({"message": "time is required"})
        
        description = data['description']
        if not description:
            return make_response(jsonify({"message": "description is required"}))
        
        if current_user.has_role('admin'):
            service.name = name
            service.description = description
            service.price = price
            service.time_required = time_required
        
        db.session.commit()
        return jsonify({"message": "Updated the specific Service", 'id': id})
    
    @roles_accepted('admin')
    def delete(self, id):
        service = Service.query.filter_by(id=id).first()
        
        if service:
            db.session.delete(service)
            db.session.commit()

            return jsonify({"message": "delete specific service", 'id': id}, 200)
       
        
    
def raw(text): #to convert the searched word to raw string
    split_list = text.split() #converts to a list
    search_word = ''
    for word in split_list:
        search_word += word.lower()
    return search_word