"""
    Commands executed through the bin/crawley script 
"""

from __future__ import with_statement

import sys
import shutil
import os.path

from utils import generate_template, get_full_template_path

generators = {}

def generator(f):
    
    generators[f.__name__] = f
    
    def decorated(*args, **kwargs):
        f(*args, **kwargs)
    
    return decorated


@generator
def startproject(*args):
    
    if len(args) < 1:
        print "No given project name"
        sys.exit(1)
    
    project_name = args[0]
    
    if not os.path.exists(project_name):
        shutil.os.mkdir(project_name)
            
    shutil.copy(get_full_template_path("manage"), project_name)    
    generate_template("settings", project_name, project_name)
    
    crawler_dir = os.path.join(project_name, project_name)
    if not os.path.exists(crawler_dir):
        shutil.os.mkdir(crawler_dir)
        
    generate_template("models", project_name, crawler_dir)
    generate_template("crawlers", project_name, crawler_dir)
