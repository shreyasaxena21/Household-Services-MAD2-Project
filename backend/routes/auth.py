from flask_restful import Resource
from flask import jsonify, make_response, request
from flask_security import verify_password, roles_accepted, current_user, logout_user, hash_password, login_required
from backend.models import userdatastore, db, Role,User

#-----------------------------------------------Login--------------------------------------------------------------
class Login(Resource):
    def post(self):
        data = request.get_json()
        # email = data.get('email')
        email = data['email']
        password = data['password']
        print(email, password)
        user = userdatastore.find_user(email=email)
        name = user.fullname
        if user:
            if user.is_approved == 0:
                return make_response(jsonify({'message': 'User account is inactive because the documents are under verification. Please have patience!.'}), 403)
            
            if verify_password(password, user.password):
                token = user.get_auth_token()
                # Role checking with debug prints
                if user.has_role('admin'):
                    role = 'admin'
                    print("User has the 'admin' role.")
                elif user.has_role('service_professional'):
                    role = 'service_professional'
                    print("User has the 'service_professional' role.")
                else:
                    role = 'customer'
                    print("User has the 'customer' role.")
                return make_response(jsonify({'token': token, 'email': user.email ,'role' : role ,'id' : user.id ,'name' : name,'message' : 'login successful'}), 200)
            return make_response(jsonify({'message': 'Password does not match, Please try again :(', 'password': password}), 401)
        return make_response(jsonify({'message': 'User doest not Exist', 'email': email}), 401)


#-----------------------------------------------Register--------------------------------------------------------------
class Register(Resource):
    def post(self):
        data = request.form
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')
        name = data.get('name')
        city= data.get('city')
        pincode = data.get('pincode')
        mobileNo = data.get('mobileNo')
        experience = data.get('experience')
        serviceType = data.get('serviceType')
        description = data.get('description')
        location = data.get('location')

        # image = request.files['image']

      
        if not email:
            return make_response(jsonify({"message": "email is required"}), 400)
        if not password:
            return make_response(jsonify({"message": "password is required"}), 400)
        if not role:
            return make_response(jsonify({"message": "role is required"}), 400)
        
        
        user = userdatastore.find_user(email=email)
        if user:
            return make_response(jsonify({"message": "user already present", "email": user.email}), 400)
        
        user = userdatastore.create_user(email=email, password=hash_password(password), fullname = name,  city = city, pincode = pincode, mobile_no = mobileNo, description = description, service_type = serviceType, experience = experience, is_approved=1)  
        
        if role == 'service_professional':
            userdatastore.deactivate_user(user)
            userdatastore.add_role_to_user(user, 'service_professional')
            user.is_approved = 0
            user.city = location
            # userdatastore.add_role_to_user(user, 'customer')
        userdatastore.add_role_to_user(user, role)
        db.session.commit()
        # user_id = user.id
        # filename = f"{user_id}.jpg"
        # print(filename)
        # image_path = os.path.join('instance/profdocs', filename)
        # image.save(image_path)
            

        return make_response(jsonify({"message": "user created successfully", "email": user.email}), 201)



#-----------------------------------------------Logout--------------------------------------------------------------
class Logout(Resource):
    @roles_accepted('admin', 'service_professional', 'customer')
    def post(self):
        user = userdatastore.find_user(id=current_user.id)
        if not user:
            return make_response(jsonify({"message": "No user found by that id"}), 404)
        logout_user(user)
        db.session.commit()
        return make_response(jsonify({"message": "user logged out successfully", "email": user.email}), 200)
    


#-----------------------------------------------Admin--------------------------------------------------------------
class GetUsers(Resource): 
    @roles_accepted('admin')
    def get(self):
        user = user = User.query.filter(User.roles.any(name='customer'), User.active==1).offset(1)
        data = []
        for users in user:
            user1 = {
                    'id': users.id,
                    'name': users.fullname,
                    'email': users.email,
                    'city' : users.city,
                    'mobno' : users.mobile_no
                }
            data.append(user1)
        print(data)
        if data == []:
            return make_response(jsonify({"message": "No User found"}), 404)
        return make_response(jsonify({"message": "get all users", "data": data}), 200)
    
class Getblockedusers(Resource): 
    @roles_accepted('admin')
    def get(self):
        user = user = User.query.filter(User.active==0, User.is_approved==1).all()
        data = []
        for users in user:
            user1 = {
                    'id': users.id,
                    'name': users.fullname,
                    'email': users.email,
                }
            data.append(user1)
        print(data)
        if data == []:
            return make_response(jsonify({"message": "No User found"}), 404)
        return make_response(jsonify({"message": "get all users", "data": data}), 200)

class GetProfessionals(Resource): 
    @roles_accepted('admin')
    def get(self):
        users = User.query.filter_by(active=0, is_approved = 0)
        data = []
        for user in users:
            user1 = {
                    'id': user.id,
                    'name': user.fullname,
                    'email': user.email,
                    'service_type' : user.service_type,
                    'experience' : user.experience,
                    'description' : user.description,
                    'location' : user.city
                }
            data.append(user1)
        print(data)
        if data == []:
            return make_response(jsonify({"message": "No User found"}), 404)
        return make_response(jsonify({"message": "Found the professionals", "data": data}), 200)

class ApproveProfessionals(Resource): 
    @roles_accepted('admin')
    def put(self, id):
        data = request.get_json()
        is_approved = data['is_approved']
        active = data['active']
        user = User.query.filter_by(id = id).first()
        if user:
            user.active = active
            user.is_approved = is_approved
            db.session.commit()
            print(user.active)
            print(user.is_approved)
            return make_response(jsonify({"message": "Professional approved successfully"}), 200)
    
    
class FlagUser(Resource): 
    @roles_accepted('admin')
    def put(self, id):
        data  = request.get_json()
        active = data['active']
        user = User.query.filter_by(id=id).first()
        
        user.active = active
        db.session.commit()
        return make_response(jsonify({"message": "User Flagged successfully"}), 200)


class Unblock(Resource): 
    @roles_accepted('admin')
    def put(self, id):
        data  = request.get_json()
        active = data['active']
        user = User.query.filter_by(id=id).first()
        
        user.active = active
        db.session.commit()
        return make_response(jsonify({"message": "User Unblocked successfully"}), 200)
    

class AdminSearch(Resource):
    @roles_accepted('admin')
    def get(self,query):
        # formatted_query = query.replace(" ", "").lower()
        search = "%{}%".format(query)
        if search:
            print(search)
            # services = Service.query.filter(Service.name.like(search)).all()
            users = User.query.filter(User.fullname.like(search), User.roles.any(name='service_professional')).all()

            searched_user=[]

            # for service in services:
            #     d={
            #         "sid":service.id,
            #         "sname":service.name,
            #     }
            #     service.append(d)

            for user in users:
                d={
                    "id": user.id,
                    "name":user.fullname,
                    "service_type" : user.service_type 
                }
                searched_user.append(d)
                return make_response(jsonify({"user":searched_user}),200)
            return make_response(jsonify({"user":[]}),200)
    
     

    
#-----------------------------------------------Customer--------------------------------------------------------------

class EditCustomerProfile(Resource):
    @roles_accepted('customer')
    def put(self, id):
        customer = User.query.filter_by(id = id).first()

        if not customer:
            return make_response(jsonify({"message" : "No Customer found by that id"}), 404)
        
        data = request.get_json()
        name = data['name']
        if not name:
            return jsonify({"message": "name is required"})
        
        city = data['city']
        if not city:
            return jsonify({"message": "city is required"})
        
        pincode = data['pincode']
        if not pincode:
            return jsonify({"message": "pincode is required"})
        
        mobileno = data['mobileno']
        if not mobileno:
            return make_response(jsonify({"message": "mobileno is required"}))
        
        if current_user.has_role('customer'):
            customer.fullname = name
            customer.city = city
            customer.pincode = pincode
            customer.mobile_no = mobileno
        
        db.session.commit()
        return jsonify({"message": "Updated the specific customer", 'id': id})
    

#-----------------------------------------------Service Professional--------------------------------------------------------------

class EditProfessionalProfile(Resource):
    @roles_accepted('service_professional')
    def put(self, id):
        professional = User.query.filter_by(id = id).first()

        if not professional:
            return make_response(jsonify({"message" : "No professional found by that id"}), 404)
        
        data = request.get_json()
        name = data['name']
        if not name:
            return jsonify({"message": "name is required"})
        
        service_type = data['service_type']
        if not service_type:
            return jsonify({"message": "service_type is required"})
        
        experience = data['experience']
        if not experience:
            return make_response(jsonify({"message": "experience is required"}))
        
        if current_user.has_role('customer'):
            professional.fullname = name
            professional.service_type = service_type
            professional.experience = experience
        
        db.session.commit()
        return jsonify({"message": "Updated the specific customer", 'id': id})
    
class GetSpecificProfessional(Resource): 
    @roles_accepted('service_professional')
    def get(self, id):
        user = user = User.query.filter(User.roles.any(name='service_professional'), User.id == id).first()
        
        user1 = {
                'id': user.id,
                'name': user.fullname,
                'email': user.email,
                'service_type' : user.service_type,
                'experience' : user.experience,
                'location' : user.city
            }
        if not user:
            return make_response(jsonify({"message" : "No User found by that id"}), 404)
        
        return make_response(jsonify({"message" : "get specific user", "data" : user1}), 200)


#-----------------------------------------------Common--------------------------------------------------------------
class GetSpecificCustomer(Resource): 
    @roles_accepted('admin', 'customer')
    def get(self, id):
        user = user = User.query.filter(User.roles.any(name='customer'), User.id == id).first()
        
        user1 = {
                'id': user.id,
                'name': user.fullname,
                'email': user.email,
                'city' : user.city,
                'mobno' : user.mobile_no,
                'pincode' : user.pincode
            }
        if not user:
            return make_response(jsonify({"message" : "No User found by that id"}), 404)
        
        return make_response(jsonify({"message" : "get specific service", "data" : user1}), 200)
        
class GetActiveProf(Resource): 
    @roles_accepted('admin', 'customer', 'service_professional')
    def get(self):
        user = user = User.query.filter(User.roles.any(name='service_professional'), User.active == 1, User.is_approved==1).all()
        data = []
        for users in user:
            user1 = {
                    'id': users.id,
                    'name': users.fullname,
                    'email': users.email,
                    'service_type' : users.service_type,
                    'experience' : users.experience,
                    'date_created' : users.date_created,
                    # 'location' : user.city
                    
                }
            data.append(user1)
        print(data)
        if data == []:
            return make_response(jsonify({"message": "No Professional found"}), 404)
        return make_response(jsonify({"message": "get all professionals", "data": data}), 200)


