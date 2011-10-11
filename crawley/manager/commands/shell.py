from crawley.crawlers import BaseCrawler 
from crawley.extractors import XPathExtractor

from command import BaseCommand
from crawley.manager.utils import exit_with_error


class ShellCommand(BaseCommand):
    """
        Shows an url data in a console like the XPathExtractor see it.
        So users can interactive scrape the data.
    """
    
    name = "shell"
    
    def validations(self):
        
        return [(len(self.args) >= 1, "No given url")]
    
    def execute(self):            
            
        try:
            import IPython
        except ImportError:
            exit_with_error("Please install the ipython console")
        
        url = self.args[0]
        crawler = BaseCrawler()
        
        data = crawler._get_data(url)
        html = XPathExtractor().get_object(data)
        
        shell = IPython.Shell.IPShellEmbed(argv=[], user_ns={ 'html' : html })
        shell()
