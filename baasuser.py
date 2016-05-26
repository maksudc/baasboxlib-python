from .baascomponent import BaasComponent
import baasbox
from .baasresult import parse_response

import enum
import json

class SCOPE(enum.Enum):
    PUBLIC = "PUBLIC"
    REGISTERED = "REGISTERED"
    FRIEND = "FRIEND"
    PRIVATE = "PRIVATE"
    
    def __unicode__(self):
        return self.name
    
#SCOPE = enum.Enum( 'PUBLIC' , 'REGISTERED' , 'FRIEND' , 'PRIVATE' )

SCOPE_FIELD_MAP = {
        
            SCOPE.PUBLIC: "visibleByAnonymousUsers",
            SCOPE.REGISTERED: "visibleByRegisteredUsers",
            SCOPE.FRIEND: "visibleByFriends",
            SCOPE.PRIVATE: "visibleByTheUser"
}

class BaasUser(BaasComponent):
    
    def __init__(self , *args , **kwargs):
        super(BaasUser , self).__init__(*args , **kwargs)
        
        self.__dict__.update(kwargs.get("content"  , {}))

    def get_token(self):
        return getattr( self , "X-BB-SESSION" , None )
    
    def set_token(self , token):
        setattr(self , "X-BB-SESSION" , token) 
    
    def get_id(self):
        return getattr(self , "id" , None)
    
    def set_id(self , id):
        setattr(self , "id" , id)
    
    def get_scope(self , scope ):        
        return getattr(self , SCOPE_FIELD_MAP.get( scope ) , None)
    
    def set_scope(self , scope , data):
        setattr(self , SCOPE_FIELD_MAP.get(scope) , data)
    
    def get_username(self):
        
        user_data =  getattr(self , 'user' , {})
        return user_data.get('name' , None)
    
    def set_username(self , username):
        user_data =  getattr(self , 'user' , {})
        user_data.update({
            'name': username
        })
        setattr(self , 'user' , user_data)
    
    def get_password(self):
        user_data =  getattr(self , 'user' , {})
        return user_data.get('password' , None)
    
    def set_password(self , password):
        user_data =  getattr(self , 'user' , {})
        user_data.update({
            'password': password
        })
        setattr(self , 'user' , user_data)
    
    def get_profile_id(self):
        return self.get_scope(SCOPE.PUBLIC).get("profileId" , None)


def login(username , password , box=None):
    
    if box == None:
        box = baasbox.get_default()
        
    url = "login"
    
    data = {
        'username': username,
        'password': password,
        'appcode': box.appcode
    }
    
    response = box.send(url , method="POST" , data=data)
    
    result_obj = parse_response(response)
    
    user = None
    if result_obj.is_success():
        user = BaasUser( content = result_obj.get_value() )
        user.set_password(password)
        user.set_username(username)
    
    if user:
        box.set_user(user)
        
    return user

def exists(username , box=None):
    if box == None:
        box = baasbox.get_default()
    
    url="plugin/account.checker.plugin"
    
    data = {
        'username': username
    }
    
    response = box.send( url , method="GET" , data=data )
    result_obj = parse_response(response)
    
    if result_obj:
        value = result_obj.get_value()
        if value:
            return value["exists"]
    
    return None

def signup(user_obj , box=None):
    
    # Signup the user
    
    user = None
    
    url = "user"
    data = {
            
        'username': user_obj.get_username(),
        'password': user_obj.get_password()
    }
    
    for scope_item_key in SCOPE_FIELD_MAP:
        
        scope_item = SCOPE_FIELD_MAP.get(scope_item_key)
        scope_value = user_obj.get_scope( scope_item_key )
        
        data[scope_item] = scope_value
    
    response = box.send(url , method="POST" , json=data)
    result_obj = parse_response(response)
    
    if result_obj:
        user = BaasUser( content = result_obj.get_value() )
        
        user.set_password( user_obj.get_password() )
        user.set_username( user_obj.get_username() )
    
    return user 

def update(user_obj , box=None):
    
    user = None
    
    url = "me"
    
    data = {}
    for scope_item_key in SCOPE_FIELD_MAP:
        
        scope_item = SCOPE_FIELD_MAP.get(scope_item_key)
        scope_value = user_obj.get_scope( scope_item_key )
        
        data[scope_item] = scope_value
    
    response = box.send(url , method="PUT" , json=data)
    result_obj = parse_response(response)
    
    if result_obj:
        user = BaasUser( content = result_obj.get_value() )
        
        user.set_password( user_obj.get_password() )
        user.set_username( user_obj.get_username() )
    
    return user 
    
    