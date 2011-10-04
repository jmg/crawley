import unittest
from crawley.manager.commands.run import RunCommand
from crawley.manager.commands.syncdb import SyncDbCommand
from crawley.manager.commands.startproject import StartProjectCommand
from crawley.manager.commands.shell import ShellCommand
import os
import shutil

class CommandsTest(unittest.TestCase):        
    
    def setUp(self):
        
        settings_dir = os.path.join(os.getcwd(), "tests", "test_project", "settings.py")
        self.settings_args = ["-s", settings_dir]
        
        self.test_name_args = ["test"]
    
    def test_startproject(self):
        
        cmd = StartProjectCommand(self.test_name_args)
        cmd.checked_execute()
        self.assertTrue(os.path.exists("test"))
        self.assertTrue(os.path.exists(os.path.join("test", "settings.py")))        
        self.assertTrue(os.path.exists(os.path.join("test", "test", "models.py")))
        self.assertTrue(os.path.exists(os.path.join("test", "test", "crawlers.py")))        
        shutil.rmtree("test")
    
    def test_syncbd(self):
                
        cmd = SyncDbCommand(self.settings_args)
        cmd.checked_execute()
        self.assertTrue(os.path.exists("test_project.sqlite"))
        os.remove("test_project.sqlite")
        
    def test_run(self):
        
        cmd = RunCommand(self.settings_args)
        cmd.checked_execute()

    def _test_shell(self):        
        """
            Skiped because it blocks the console
        """
        
        cmd = ShellCommand(self.test_name_args)
        cmd.checked_execute()              
