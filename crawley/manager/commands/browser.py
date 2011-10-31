import sys
from PyQt4 import QtGui
from command import BaseCommand
from crawley.utils import exit_with_error

from crawley.web_browser.browser import Browser

class BrowserCommand(BaseCommand):
    """
        Runs a browser
    """
    
    name = "browser"
    
    def validations(self):
        
        return [(len(self.args) >= 1, "No given url")]
    
    def execute(self):            
            
        app = QtGui.QApplication(sys.argv)
        main = Browser(self.args[0])
        main.show()
        sys.exit(app.exec_())
        
