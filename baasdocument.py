from .baascomponent import BaasComponent
from .baasbox import get_default
from .baasresult import parse_response
import os
import enum

class ACTION(enum.Enum):
    read = "read"
    update = "update"
    delete = "delete"
    all = "all"
    
    def __unicode__(self):
        return self.name
    
#ACTION = enum.Enum( 'read' , 'update' , 'delete' , 'all' )

class ROLE(enum.Enum):
    anonymous = "anonymous"
    registered = "registered"
    private  = "private"
    
    def __unicode__(self):
        return self.name
    
#ROLE = enum.Enum( 'anonymous' , 'registered' , 'private')

class BaasDocument(BaasComponent):
    
    endpoint =  os.path.join("document")
    
    KEY_CLASS = "@class"
    KEY_RID = "@rid"
    KEY_VERSION ="@version"
    
    KEY_ID = "id"
    KEY_CREATION_DATE = "_creation_date"
    KEY_AUTHOR = "_author"
    
    def __init__(self , *args , **kwargs):
        super(BaasDocument , self).__init__(*args ,**kwargs)
        
        self.__dict__.update(kwargs.get("content" , {}))
        
    
    def save(self ,**kwargs):
         
        box = kwargs.get( 'box' , None)
        
        self.endpoint = self.endpoint + "/" + box.get_collection()
         
        # Check the id , if the id is present it is an update
        document_id = getattr( self , self.KEY_ID , None )
        
        updated = False
        
        if document_id:            
            # Since it is an update request. So only body of the document should nbe inside the request since 
            # Other meta datas can not be updated and should not be available in the body pf update request
            json_body = self.get_document_body()
            
            url = os.path.join( self.endpoint , document_id )
            
            response = box.send( url , method="PUT" , json=json_body ) 
            
            result_obj = parse_response(response)
            
            if result_obj.is_success():
                updated = True
                
                value = result_obj.get_value()
                
                if isinstance( value , dict ):
                    self.__dict__.update( value )
        else:
            json_body = self.get_document_body()
            url = self.endpoint
            
            response = box.send( url , method="POST" , json=json_body )
            
            result_obj = parse_response(response)
            
            if result_obj.is_success():
                updated = True
                
                value = result_obj.get_value()
                
                if isinstance( value , dict ):
                    self.__dict__.update( value )
        
        if updated:
            return self
        else: 
            return None
    
    def get_meta_data(self):
        
        json_dict = {
            self.KEY_CLASS: getattr(self, self.KEY_CLASS , None),
            self.KEY_RID: getattr(self , self.KEY_RID , None),
            self.KEY_VERSION : getattr(self , self.KEY_VERSION , None),
            
            self.KEY_ID: getattr(self , self.KEY_ID , None),
            
            self.KEY_CREATION_DATE: getattr(self , self.KEY_CREATION_DATE , None),
            self.KEY_AUTHOR: getattr(self , self.KEY_AUTHOR , None),
        }
        
        return json_dict
    
    def get_document_body(self):
        
        json_dict = {}
        return json_dict
        
    
    def to_json(self):
        
        json_dict = {}
        json_dict.update( self.get_meta_data() )
        json_dict.update( self.get_document_body() )
        
        return json_dict
        
    
def fetch_all(**kwargs):
    
    box = kwargs.get('box')
    criteria = kwargs.get("criteria" , "")
    
    fetch_url = BaasDocument.endpoint + "/" + box.get_collection()
    
    if criteria:
        fetch_url = fetch_url + "?" + "where="+ criteria
    
    
    #parse the response to send link object or raise error
    response = box.send( fetch_url  , method="GET" )
    
    result_obj = parse_response(response)
    
    link_obj = []
    
    if result_obj.is_success():
        value = result_obj.get_value()
         
        if isinstance( value , list):
            for value_item in value:
                link_obj.append(BaasDocument(content = value_item))
        
        if isinstance(value , dict):
            link_obj = BaasDocument(content = value) 
                
    return link_obj
    
    
    #parse the response to send link object
            
def fetch(id , box = None, recordsPerPage=None , skip=None, where =None ,params=None,orderBy=None , page=None,fields=None,groupBy=None,count=None):
    
    fetch_url = BaasDocument.endpoint + "/" +box.get_collection()
    
    if id:
        fetch_url = fetch_url + "/" + id
            
    fetch_url = fetch_url + "?"
    
    query_string_attached = False
    
    if recordsPerPage:
        fetch_url = fetch_url + "recordsPerPage="+ unicode(recordsPerPage)
        query_string_attached = True
    
    if skip:
        if query_string_attached:
            fetch_url = fetch_url + "&"
        fetch_url = fetch_url + "skip="+ unicode(skip)
    
    if where:
        if query_string_attached:
            fetch_url = fetch_url + "&"
        fetch_url = fetch_url + "where="+ unicode(where)
    
    if params:
        if query_string_attached:
            fetch_url = fetch_url + "&"
        fetch_url = fetch_url + "params="+ unicode(params)
    
    if orderBy:
        if query_string_attached:
            fetch_url = fetch_url + "&"
        fetch_url = fetch_url + "orderBy="+ unicode(orderBy)
    
    if page != None:
        if query_string_attached:
            fetch_url = fetch_url + "&"
        fetch_url = fetch_url + "page="+ unicode(page)
    
    if fields:
        if query_string_attached:
            fetch_url = fetch_url + "&"
        fetch_url = fetch_url + "fields="+ unicode(fields)
    
    if groupBy:
        if query_string_attached:
            fetch_url = fetch_url + "&"
        fetch_url = fetch_url + "groupBy="+ unicode(groupBy)
    
    if count:
        if query_string_attached:
            fetch_url = fetch_url + "&"
        fetch_url = fetch_url + "count="+ unicode(count)
            
    
    #box = kwargs.get('box' , get_default())
    
    #parse the response to send link object or raise error
    # @todo need to implement further
    response = box.send(fetch_url , method="GET")
    
    result_obj = parse_response(response)
    
    link_obj = None
    
    if result_obj.is_success():
        
        value = result_obj.get_value() 
        if isinstance( value , dict):
            link_obj = BaasDocument(content = result_obj.get_value())
        
        elif isinstance( value , list ):
            if( len(value) == 1 ):
                link_obj = BaasDocument(content = value[0])
            pass
        else:
            link_obj = value
                    
    return link_obj

    
def delete(id , box=None):
    
    fetch_url = BaasDocument.endpoint + "/" + box.get_collection()
    fetch_url = fetch_url + "/" + id

    response = box.send(fetch_url , method="DELETE")
    
    result_obj = parse_response(response)
    
    link_obj = None
    
    if result_obj.is_success():
        value = result_obj.get_value() 
        if isinstance( value , dict):
            link_obj = BaasDocument(content = result_obj.get_value())
    
    if link_obj == None:
        link_obj = result_obj
    
    return link_obj

def grant(id , action , role , box=None):
    
    fetch_url = BaasDocument.endpoint + "/" + box.get_collection()
    fetch_url = fetch_url + "/" + unicode(id)
    fetch_url = fetch_url + "/" + unicode(action)
    
    fetch_url = fetch_url + "/" + "role"
    fetch_url = fetch_url + "/" + unicode(role)
    
    response = box.send(fetch_url , method="PUT")
    result_obj = parse_response(response)
    
    link_obj = None
    if result_obj.is_success():
        value = result_obj.get_value() 
        if isinstance( value , dict):
            link_obj = BaasDocument(content = result_obj.get_value())
    
    if link_obj == None:
        link_obj = result_obj
        
    return link_obj