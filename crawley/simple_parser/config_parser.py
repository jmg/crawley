import os.path
from ConfigParser import ConfigParser

CONFIG_FILE = 'config.ini'

class ConfigObj(object):
    """
        Implements a dictionary object of (section, item)
        with the config.ini file
    """

    def __init__(self):
        self._config_parser = ConfigParser()
        self.config = {}

    def _update_dictionary(self):
        for sect in self._config_parser.sections():
            for item_name, value in self._config_parser.items(sect):
                self.config[(sect, item_name)] = value

    def __getitem__(self, key):
        return self.config.get(key, None)

    def __setitem__(self, key, value):
        if value is None:
            value = ''
        self.config[key] = value
        (section, item) = key
        if not self._config_parser.has_section(section):
            self._config_parser.add_section(section)
        self._config_parser.set(section, item, value)

    def __str__(self):
        return str(self.config)

    def save(self, filename):
        self._config_parser.write(open(filename,'wb'))


class ConfigApp(ConfigObj):
    """
        Open the CONFIG_FILE and update the dictionary
        It can be accesed with a tuple of (section, item). I.E.:

        config = ConfigApp()
        value = config[('section', 'item')]
    """

    def __init__(self, ini_dir):
        
        ConfigObj.__init__(self)
        self._config_parser.readfp(open(os.path.join(ini_dir, CONFIG_FILE), 'rb'))
        self._update_dictionary()

    def save(self):
        ConfigObj.save(self, CONFIG_FILE)
