from crawley.utils.common import exit_with_error

class CustomDict(dict):    

    def __init__(self, error="[%s] Not valid argument", *args, **kwargs):

        self.error = error
        dict.__init__(self, *args, **kwargs)

    def __getitem__(self, key):

        if key in self:
            return dict.__getitem__(self, key)
        else:
            exit_with_error(self.error % key)
