from optparse import OptionParser

from command import BaseCommand
from crawley.manager.projects import project_types, CodeProject


class StartProjectCommand(BaseCommand):
    """
        Starts a new crawley project. 
        
        Copies the files inside conf/project_template in order 
        to generate a new project
    """
    
    name = "startproject"
    
    def validations(self):
                
        return [(len(self.args) >= 1, "No given project name")]

    def execute(self):                                
        
        self.parser = OptionParser()
        self.parser.add_option("-t", "--type", help="Type can be 'code' or 'template'")
        
        (options, args) = self.parser.parse_args(self.args)
        
        if options.type is None:
            options.type = CodeProject.name
            project_name = self.args[0]
        else:
            project_name = self.args[2]
        
        project = project_types[options.type]()
        project.set_up(project_name)
