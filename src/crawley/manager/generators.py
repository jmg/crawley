"""
    Commands executed through the bin/crawley script 
"""

from __future__ import with_statement

import sys
import shutil
import os.path

generators = {}

def generator(f):
    
    generators[f.__name__] = f
    
    def decorated(*args, **kwargs):
        f(*args, **kwargs)
    
    return decorated


def generate_template(tm_name, project_name):

    with open(os.path.join("crawley", "manager", "templates", "%s.tm") % tm_name, 'r') as f:
        
        template = f.read()
        data = template % { 'project_name' : project_name }
        
    with open(os.path.join(project_name, "%s.py" % tm_name), 'w') as f:
        f.write(data)
        

@generator
def startproject(*args):
    
    if len(args) < 1:
        print "No given project name"
        sys.exit(1)
    
    project_name = args[0]
    
    if not os.path.exists(project_name):
        shutil.os.mkdir(project_name)
    
    generate_template("models", project_name)
    generate_template("crawlers", project_name)
