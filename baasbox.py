import json
import requests
import base64
import os


global __default_instance__
__default_instance__ = None

class BaasBox(object):
    
    KEY_HOST = "host"
    KEY_PORT = "port"
    KEY_APPCODE = "appcode"
    KEY_PUSH_SENDER_ID = "push_sender_id"
    
    default_instance = None
    protocol = None
    host = None
    port = None
    appcode = None
    push_sender_id = None
    user = None
    configs = {}
    
    def __init__(self , *args , **kwargs):
        # Read the json config option file
        self.configs = kwargs.get('configs' , {})
        
        self.protocol = self.configs["protocol"]
        self.host = self.configs["host"]
        self.port = self.configs["port"]
        self.appcode = self.configs["appcode"]
        self.push_sender_id = self.configs["push_sender_id"]
        self.collection = self.configs["collection"]
            
        self.user = None
            
        
        # Override any settings that explicitely added while initialization
        self.__dict__.update(kwargs)
    
    def set_user(self , user):
        self.user = user
        
    def get_collection(self):
        return getattr(self , 'collection')
        
    def get_url(self):
        
        url_endpoint = ""
        
        if self.protocol == "http":
            url_endpoint = url_endpoint + "http://"
        elif self.protocol == "https":
            url_endpoint = url_endpoint + "https://"
        else:
            raise Exception("invalid protocol found")
        
        if self.host:
            url_endpoint = url_endpoint + self.host
        
        else:
            raise Exception( " Invalid Host Exception " )
        
        if self.port:
            url_endpoint = url_endpoint + ":" + unicode(self.port)
        else:
            raise Exception(" invalid port exception ")
        
        return url_endpoint
    
    
    def prepare_appcode_header(self):
        return { 'appcode': self.appcode , "X-BAASBOX-APPCODE":self.appcode }
    
    def prepare_user_session_header(self):
        session_dict = {}
        if self.user:
            if self.user.get_token():
                session_dict.update({ 'X-BB-SESSION': self.user.get_token() })
            elif self.user.get_password():
                session_dict.update({ "AUTHORIZATION": "BASIC" +" " + base64.encodestring( self.user.get_username() + ":"+ self.user.get_password() ) })
        
        if not session_dict:
            pass
            #session_dict.update({ "AUTHORIZATION": "BASIC" +" " + base64.encodestring( "baasboxlib" + ":"+ "baasboxlib" ) })
         
        return session_dict    
    
    def send(self , endpoint ,  **kwargs):
        url = self.get_url() + "/" + endpoint
        
        method = kwargs.get("method" , "GET")
        
        if method=="GET":
            
            if "?" in url:
                url = url + "&"
            else:
                url = url + "?"
 
            url = url + "X-BAASBOX-APPCODE="+ self.appcode
            
        params = kwargs.get('params' , None)
        data = kwargs.get("data" ,None)
        json_data = kwargs.get("json" , None)
        
        
        headers = {}
        headers.update(self.prepare_appcode_header())
        headers.update(self.prepare_user_session_header())
        
        headers.update(kwargs.get('headers' , {}))
        
        res = requests.api.request( method , url , headers = headers , params = params , data = data , json = json_data)
        
        return res
    
def get_default():
    
    global __default_instance__
    
    if not __default_instance__:
        __default_instance__ = BaasBox()
    
    return __default_instance__

