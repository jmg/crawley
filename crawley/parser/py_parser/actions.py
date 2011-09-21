"""
    Actions
"""

class Action(object):
    pass    

class FirstAction(Action):
    
    def __str__(self):
        return "[0]"

class LastAction(Action):
    
    def __str__(self):
        return "[-1]"

class AllAction(Action):
    
    def __str__(self):
        return ""
