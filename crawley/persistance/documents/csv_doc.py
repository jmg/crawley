import csv 
    
from meta import DocumentMeta

csv_objects = []

class CSVDocument(object):
    """
        CSV Document base class
    """
    
    __metaclass__ = DocumentMeta
    
    def __init__(self, **kwargs):
                
        csv_objects.append(kwargs)
                
                
class Session(object):
    """
        A class featuring a database session
    """
    
    file_name = None

    def commit(self):
        """
            Dumps the scraped data to the filesystem
        """
        
        with open(self.file_name, 'wb') as f:
            
            writer = csv.writer(f)
                        
            if csv_objects:
                
                titles = self._encode(csv_objects[0].keys())
                writer.writerow(titles)            
                
                for csv_object in csv_objects:
                    
                    values = self._encode(csv_object.values())
                    writer.writerow(values)
                    
    def _encode(self, list_values):
        
        return [v.encode('utf-8') for v in list_values if v is not None]
            
    def close(self):
        pass
            

session = Session()
