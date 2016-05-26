from .baascomponent import BaasComponent
from .baasbox import get_default
from .baasresult import parse_response

class BaasLink(BaasComponent):
    
    endpoint = "link"
    
    def __init__(self , *args , **kwargs):
        super(BaasLink , self).__init__(*args ,**kwargs)
        
        self.__dict__.update(kwargs.get("content" , {}))
        
    
def fetch_all(**kwargs):
    
    fetch_url = BaasLink.endpoint
    criteria = kwargs.get("criteria" , "")
    count  = kwargs.get( "count" , None )
    
    if criteria:
        fetch_url = fetch_url + "?" + "where="+ criteria + "&"
    
    if count:
        if "?" in fetch_url:
            fetch_url = fetch_url + "&"
        else:
            fetch_url = fetch_url + "?"
            
        fetch_url = fetch_url + "count=true"
    
    box = kwargs.get("box" , get_default())
    
    #parse the response to send link object or raise error
    response = box.send( fetch_url  , method="GET" )
    
    result_obj = parse_response(response)
    
    link_obj = []
    
    if result_obj.is_success():
        value = result_obj.get_value()
         
        if isinstance( value , list):
            for value_item in value:
                link_obj.append(BaasLink(content = value_item))
        
        if isinstance(value , dict):
            link_obj = BaasLink(content = value) 
                
    return link_obj
    
    
    #parse the response to send link object
            
def fetch(id , **kwargs):
    
    fetch_url = BaasLink.endpoint
    fetch_url = fetch_url + "/" + id
    
    box = kwargs.get('box' , get_default())
    
    #parse the response to send link object or raise error
    # @todo need to implement further
    response = box.send(fetch_url , method="GET")
    
    result_obj = parse_response(response)
    
    link_obj = None
    
    if result_obj.is_success():
        value = result_obj.get_value() 
        if isinstance( value , dict):
            link_obj = BaasLink(content = result_obj.get_value())
            
                
    return link_obj
    
def delete(id , **kwargs):
    
    fetch_url = BaasLink.endpoint
    fetch_url = fetch_url + "/" + id
    
    box = kwargs.get('box' , get_default())

    response = box.send(fetch_url , method="DELETE")
    
    result_obj = parse_response(response)
    
    link_obj = None
    
    if result_obj.is_success():
        value = result_obj.get_value() 
        if isinstance( value , dict):
            link_obj = BaasLink(content = result_obj.get_value())
    
    if link_obj == None:
        link_obj = result_obj
    
    return link_obj

