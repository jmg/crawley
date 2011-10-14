import simplejson
from meta import DocumentMeta

json_objects = []
file_name = "data.json"

class JSONDocument(object):
    """
        JSON Document base class
    """
    
    __metaclass__ = DocumentMeta
    
    def __init__(self, **kwargs):
                
        json_objects.append(kwargs)
                
                
class Session(object):
    """
        A class featuring a database session
    """

    def commit(self):
        """
            Dumps the scraped data to the filesystem
        """
        with open(file_name, 'w') as f:
            simplejson.dump(json_objects, f)
            
    def close(self):
        pass
            

session = Session()
