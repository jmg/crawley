documents_entities = []

class DocumentMeta(type):
    
    def __init__(cls, name, bases, dct):
        
        documents_entities.append(cls)
        super(DocumentMeta, cls).__init__(name, bases, dct)
