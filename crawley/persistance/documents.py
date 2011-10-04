from lxml import etree

root = etree.Element('root')
file_name = "data.xml"

class XMLDocument(object):
    
    def __init__(self, **kwargs):
        
        self.__dict__.update(kwargs)        
        
        row = etree.Element(self.__class__.__name__)
        root.append(row)
        
        for key, value in [(k,v) for (k,v) in self.__dict__.items() if not k.startswith("_")]:
            
            element = etree.Element(key)
            element.text = value
            row.append(element)


class Session(object):

    def commit(self):
            
        with open(file_name, "w") as f:
            f.writelines(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8'))

session = Session()
