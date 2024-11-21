from flask_security import Security, verify_password, hash_password

from backend.models import db, userdatastore

security = Security()

def login_fn(email, password):
    user = userdatastore.find_user(email=email)  
    if user:
        if verify_password(password, user.password):  
            return user.get_auth_token()
        return 'Invalid password'
    return 'User not found'

def raw(text): #to convert the searched word to raw string
    split_list = text.split() #converts to a list
    search_word = ''
    for word in split_list:
        search_word += word.lower()
    return search_word