'''
Created on Dec 17, 2015

@author: maksud
'''
import json

class BaasResult(object):
    
    def __init__(self , *args , **kwargs):
         
        self.raw_response = kwargs.get("response_body" , {})
        
        """
        self.raw_response["http_code"] = kwargs.get('http_code' , None)
        self.raw_response["result"] = kwargs.get("result" , None)
        self.raw_response["data"] = kwargs.get("data" , None)
        
        self.raw_response["message"] = kwargs.get("message" , None)
        
        self.raw_response.update(json.loads(kwargs.get("body" , "{}")))
        """     
        
    def get_http_code(self):
        return self.raw_response["http_code"]
    def get_result(self):
        return self.raw_response["result"]
    def get_data(self):
        return self.raw_response["data"]
    
    def set_http_code(self , http_code):
        self.raw_response["http_code"] = http_code
        
    def set_result(self , result):
        self.raw_response["result"] = result
    
    def set_data(self , data):
        self.raw_response["data"] = data
        
    def get_value(self):
        return self.raw_response.get("data", self.raw_response.get("message"))
    
    def is_success(self):
        return self.raw_response.has_key("data") and (self.raw_response.get("result") == "ok")
    
def parse_response(response_obj):
    
    res_status_code = response_obj.status_code
    
    result_obj = BaasResult( response_body = response_obj.json())
    
    if (res_status_code == 200) or (res_status_code==201 ) or (res_status_code == 202):
        
        pass
    else:
        raise Exception( "Exception in request: Detail in : " + unicode(response_obj.json()) )
        
    return result_obj