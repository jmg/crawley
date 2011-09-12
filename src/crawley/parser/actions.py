#Mr. Crawley Parser Actions

class Action(object):
    def __init__(self):
        raise Exception("Abstract Class")

class First(Action):
    def __str__(self):
        return "first"

class Last(Action):
    def __str__(self):
        return "last"

class For(Action):
    def __str__(self):
        return "for"

class CrawleyActionNotFoundException(Exception):
    def __init__(self, message):
        self.message = message
