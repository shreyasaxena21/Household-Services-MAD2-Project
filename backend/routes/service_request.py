from flask_restful import Resource
from flask import jsonify, make_response, request
from flask_security import roles_accepted, current_user
from backend.models import ServiceRequest, db, Service, User
from datetime import datetime
from sqlalchemy import or_, and_


#--------------------------------------Customer--------------------------------------------------------------
class CreateServiceRequest(Resource):
    @roles_accepted('customer')
    def post(self):
        data = request.get_json()

        service_type = data.get('service_type')
        customer_id = data.get('customer_id')
        professional_id = data.get('professional_id')
        date_of_completion = datetime.strptime(data['date_of_completion'], '%Y-%m-%d').date()
        message = data.get('message')
        
        service = Service.query.filter_by(name = service_type).first()
        if service:
            service_id = service.id
        
            if current_user.has_role('customer'):
                # Create a new Service Request
                service_request = ServiceRequest(service_id = service_id, customer_id = customer_id, professional_id = professional_id, date_of_completion = date_of_completion, message = message)
        
                # Add the service to the session and commit
                db.session.add(service_request)
                db.session.commit()
                # Use the service object's id attribute
                return make_response(jsonify({
                    "message": "Service Request created successfully",
                    "id": service_request.id,  # Correctly use the service object's id
                }), 201)
        # If service is not found, return an error response
        return make_response(jsonify({"message": "Service type not found"}), 404)


class SpecificServiceRequest(Resource):
    @roles_accepted('admin', 'service_professional', 'customer')
    def get(self, id):
        service_request = ServiceRequest.query.filter_by(customer_id=id ).all() 
        data = []
        for request in service_request:
                professional = User.query.get(request.professional_id)
                professional_name = professional.fullname

                service = Service.query.get(request.service_id)
                service_name = service.name
                    

                req = {
                        'id': request.id,
                        'prof_name': professional_name,
                        'service_name': service_name,
                        'customer_id' : request.customer_id,
                        'date_of_request' : request.date_of_request,
                        'date_of_completion' : request.date_of_completion,
                        'service_status' : request.service_status,
                        'message' : request.message,
                        'remarks' : request.remarks
                    }
                data.append(req)
                print(data)
                if data == []:
                    return make_response(jsonify({"message": "No Service Request found"}), 404)
        return make_response(jsonify({"message": "get all service requests", "data": data}), 200)

    
    @roles_accepted('customer')
    def put(self, id):
        service_request = ServiceRequest.query.filter_by(id = id).first()

        if not service_request:
            return make_response(jsonify({"message" : "No Service Request found by that id"}), 404)
        
        data = request.get_json()
        date_of_completion = data['date_of_completion']
        if not date_of_completion:
            return jsonify({"message": "Date of Completion is required"})
        
        service_status = data['service_status']
        if not service_status:
            return jsonify({"message": "Service Status is required"})
        
        remarks = data['remarks']
        if not remarks:
            return jsonify({"message": "Remarks are required"})
        
        if current_user.has_role('customer'):
            service_request.date_of_completion = date_of_completion
            service_request.service_status = service_status
            service_request.remarks = remarks
        
        db.session.commit()
        return jsonify({"message": "Updated the specific Service Request", 'id': id})
    
class GetServiceRequest(Resource):
    @roles_accepted('customer')
    def get(self, id):
        service_request = ServiceRequest.query.filter(ServiceRequest.customer_id == id).first()  
        
        req = {
                'id': service_request.id,
                'date_of_completion' : service_request.date_of_completion,
                'service_status' : service_request.service_status,
                'remarks' : service_request.remarks
            }
        
        if not service_request:
            return make_response(jsonify({"message" : "No Service found by that id"}), 404)
        
        return make_response(jsonify({"message" : "get specific service", "data" : req}), 200)
    
               

class CloseServiceRequest(Resource):
    @roles_accepted('customer')
    def put(self, id):
        service_request = ServiceRequest.query.filter_by(id=id).first()
        data = request.get_json()
        service_status = data['service_status']
        remarks = data['remarks']
        if current_user.has_role('customer'):
            service_request.service_status = service_status
            service_request.remarks = remarks
            db.session.commit()
            return jsonify({"message": "Closed specific service", 'id': id}, 200)

class GetCompletedRequests(Resource):  
    @roles_accepted('customer')
    def get(self):
        service_request = ServiceRequest.query.filter(ServiceRequest.service_status == "Completed").all()

        data = []
        for request in service_request:
            professional = User.query.get(request.professional_id)
            professional_name = professional.fullname

            service = Service.query.get(request.service_id)
            service_name = service.name
                

            req = {
                    'id': request.id,
                    'prof_name': professional_name,
                    'service_name': service_name,
                    'customer_id' : request.customer_id,
                    'date_of_request' : request.date_of_request,
                    'date_of_completion' : request.date_of_completion,
                    'service_status' : request.service_status,
                    'message' : request.message,
                    'remarks' : request.remarks
                }
            data.append(req)
        print(data)
        if data == []:
            return make_response(jsonify({"message": "No Service Request found"}), 404)
        return make_response(jsonify({"message": "get all service requests", "data": data}), 200)


#-----------------------------------------------------Service Professional------------------------------------------------------   
class GetCustomerRequests(Resource):
    @roles_accepted('service_professional')
    def get(self, id):
        service_request = ServiceRequest.query.filter_by(professional_id = id, service_status = "Pending").all()

        data = [] 
        for request in service_request:
            customer = User.query.get(request.customer_id)
            customer_name = customer.fullname
            customer_location = customer.city
            pincode = customer.pincode

            service = Service.query.get(request.service_id)
            service_name = service.name

            req = {
                'id' : request.id,
                'cust_name' : customer_name,
                'cust_city' : customer_location,
                'pincode' : pincode,
                'service_name' : service_name,
                'date_of_request' : request.date_of_request,
                'date_of_completion' : request.date_of_completion,
                'service_status' : request.service_status,
                'message' : request.message
            }
            data.append(req)
        print(data)
        if data == []:
            return make_response(jsonify({"message": "No Customer Request found"}), 404)
        return make_response(jsonify({"message": "get all customer requests", "data": data}), 200)
    
class GetAcceptedRequests(Resource):
    @roles_accepted('service_professional')
    def get(self, id):
        service_request = ServiceRequest.query.filter(ServiceRequest.professional_id == id, or_(ServiceRequest.service_status == "Assigned", ServiceRequest.service_status == "Completed")).all()
        data = [] 
        for request in service_request:
            customer = User.query.get(request.customer_id)
            customer_name = customer.fullname
            customer_location = customer.city
            pincode = customer.pincode

            service = Service.query.get(request.service_id)
            service_name = service.name

            req = {
                'id' : request.id,
                'cust_name' : customer_name,
                'cust_city' : customer_location,
                'pincode' : pincode,
                'service_name' : service_name,
                'date_of_request' : request.date_of_request,
                'date_of_completion' : request.date_of_completion,
                'service_status' : request.service_status,
                'message' : request.message
            }
            data.append(req)
        print(data)
        if data == []:
            return make_response(jsonify({"message": "No Customer Request found"}), 404)
        return make_response(jsonify({"message": "get all customer requests", "data": data}), 200)
    

class AcceptRequest(Resource):
    @roles_accepted('service_professional')
    def put(self, id):
        data = request.get_json()
        service_status = data['service_status']
        s_request = ServiceRequest.query.filter_by(id = id).first()
        if current_user.has_role('service_professional'):
            s_request.service_status = service_status
            db.session.commit()
            return jsonify({"message": "Accepted customer request", 'id': id}, 200)


class RejectRequest(Resource):
    @roles_accepted('service_professional')
    def put(self, id):
        data = request.get_json()
        service_status = data['service_status']
        s_request = ServiceRequest.query.filter_by(id = id).first()
        if current_user.has_role('service_professional'):
            s_request.service_status = service_status
            db.session.commit()
            return jsonify({"message": "Accepted customer request", 'id': id}, 200)
    


    


        