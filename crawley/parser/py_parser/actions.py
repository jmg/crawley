"""
    Actions
"""

class Action(object):
    
    @classmethod
    def populateActions(self):
        
        actionElements = {}
        actionElements["first"] = FirstAction()
        actionElements["last"] = LastAction()
        actionElements["all"] = AllAction()
        return actionElements
    
    @classmethod
    def getAction(self, action):
        return self.populateActions().get(action)
        

class FirstAction(Action):
    
    def __str__(self):
        return "[0]"

class LastAction(Action):
    
    def __str__(self):
        return "[-1]"

class AllAction(Action):
    
    def __str__(self):
        return ""
