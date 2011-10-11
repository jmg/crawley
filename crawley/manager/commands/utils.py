import sys
import os

PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(PATH, "..", "..", "conf", "project_template")


def exit_with_error(error="Non Specified Error"):
    """
        Terminates crawley with an error
    """
    print error
    sys.exit(1)


def import_user_module(module):
    """
        Imports a user module
    """
    
    try:
        return __import__(module, locals(), globals(), [])
    except ImportError:
        print "%s.py file not found!" % module
        sys.exit(1)  
   
        
def search_class(base_klass, entities_list, return_class=False):
    
    for klass in entities_list:
        if issubclass(klass, base_klass) and not klass is base_klass:            
            return klass        


def generate_template(tm_name, project_name, output_dir):
    """
        Generates a project's file from a template 
    """

    with open(os.path.join(TEMPLATES_DIR, "%s.py") % tm_name, 'r') as f:
        
        template = f.read()
        data = template % { 'project_name' : project_name }
        
    with open(os.path.join(output_dir, "%s.py" % tm_name), 'w') as f:
        f.write(data)


def get_full_template_path(tm_name):
    """
        Returns the full template path 
    """
    
    return os.path.join(TEMPLATES_DIR, "%s.py" % tm_name)


