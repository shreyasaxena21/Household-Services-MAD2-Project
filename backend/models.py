from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore, AsaList
from sqlalchemy.ext.mutable import MutableList
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True)
    fullname = db.Column(db.String)
    search_name = db.Column(db.String, nullable = False, default="null")
    email = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)
    fs_uniquifier = db.Column(db.String, unique = True, nullable = False)
    active = db.Column(db.Boolean, default = 1)
    is_approved = db.Column(db.Boolean, default = 0)
    # search_name = db.Column(db.String, nullable = False, default="null")
    # search_location = db.Column(db.String, nullable = False, default="null")

    #customer
    city = db.Column(db.String, nullable = True)
    pincode =  db.Column(db.Integer, nullable = True)
    mobile_no = db.Column(db.Integer, nullable = True)
    
    #service professional
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    description = db.Column(db.String, nullable = True)
    service_type = db.Column(db.String, nullable = True)
    experience =  db.Column(db.String, nullable = True)
    location = db.Column(db.String, nullable = True)


    #Relationships
    roles = db.relationship('Role', backref = 'bearers', secondary = 'user_roles')
    services = db.relationship('Service', backref='professional')  # Professional services
    
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'name' : self.name,
            'active': self.active,
            'fs_uniquifier': self.fs_uniquifier,
            'city' : self.city,
            'pincode' : self.pincode,
            'mobile number' : self.mobile_no,
            'date created' : self.date_created,
            'description' : self.description,
            'service_type' : self.service_type,
            'experience' : self.experience,
            'is_approved' : self.is_approved,
            'roles': [role.name for role in self.roles]
        }
    
    def get_all_users():
        users = User.query.all()
        return users





class Role(db.Model, RoleMixin):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, unique = True, nullable = False)
    description = db.Column(db.String, nullable = False)
    permissions = db.Column(MutableList.as_mutable(AsaList()), nullable=True)

class UserRoles(db.Model):
    __tablename__ = "user_roles"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))


userdatastore = SQLAlchemyUserDatastore(db, User, Role)

class Service(db.Model):
    __tablename__ = "service"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, unique=True)
    search_name = db.Column(db.String, nullable = False, default="null")
    price = db.Column(db.Float, nullable = True)
    time_required = db.Column(db.Integer, nullable = True) # Time in hours
    description = db.Column(db.String, nullable = True)
    image = db.Column(db.String, nullable = True)
    prof_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    # search_name = db.Column(db.String, nullable = False, default="null")


    #Relationships
    service_requests = db.relationship('ServiceRequest', backref = 'service')
    # professional = db.relationship('User', backref='services', foreign_keys=[prof_id])  # Adding relationship with User model

    def serialize(self):
        return{
            'id' : self.id,
            'name' : self.name,
            'price' : self.price,
            'time required' : self.time_required,
            'image' : self.image,
            'prof_id' : self.prof_id

        }
    
    def admin_delete(id):
        service = Service.query.filter_by(id=id).first()
        if not service:
            return "No Service found by that id", False
        # delete category row with sql
        db.session.delete(service)
        db.session.commit()
        return "Category deleted successfully", True


class ServiceRequest(db.Model):
    __tablename__ = "service_request"
    id = db.Column(db.Integer, primary_key = True)
    service_id = db.Column(db.Integer, db.ForeignKey("service.id"), nullable = False)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    professional_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    date_of_request = db.Column(db.DateTime, default = datetime.utcnow)
    date_of_completion = db.Column(db.String, nullable = False)
    service_status = db.Column(db.String, default = 'Pending') # Pending # Completed # Closed
    remarks = db.Column(db.Text, nullable = True)
    message = db.Column(db.Text)
    # search_name = db.Column(db.String, nullable = False, default="null")

    # service = db.relationship('Service',  backref='service_requests')
    customer = db.relationship('User', foreign_keys=[customer_id])
    professional = db.relationship('User', foreign_keys=[professional_id])

    def serialize(self):
        return {
            'id': self.id,
            'service_id': self.service_id,
            'customer_id' :self.customer_id,
            'professional_id': self.professional_id,
            'date_of_request': self.date_of_request,
            'date_of_completion' : self.date_of_completion,
            'service_status' : self.service_status,
            'remarks' : self.remarks,
            'message' : self.message,
            'customer' : [customer.id for customer in self.customer],
            'professional': [prof.id for prof in self.professional],
            
        }

    
    

