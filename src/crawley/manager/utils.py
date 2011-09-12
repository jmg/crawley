import sys

def import_user_module(module):
    
    try:
        return __import__(module, locals(), globals(), [])
    except ImportError:
        print "%s.py file not found!" % module
        sys.exit(1)  

def inspect_module(module, klass, get_first=False):
        
    objects = []
    for k,v in module.__dict__.iteritems():
        try:
            if issubclass(v, klass) and v is not klass:
                if get_first:
                    return v
                objects.append(v)
        except:
            pass
    if get_first:
        return None
    return objects
