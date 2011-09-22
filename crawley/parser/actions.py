"""
    Actions
"""

class Action(dict):
    
    def __init__(self):
        dict.__init__(self)
        self["first"] = FirstAction().__str__()
        self["last"] = LastAction().__str__()
        self["all"] = AllAction().__str__()

class FirstAction(object):
    
    def __str__(self):
        return "[0]"

class LastAction(object):
    
    def __str__(self):
        return "[-1]"

class AllAction(object):
    
    def __str__(self):
        return ""
