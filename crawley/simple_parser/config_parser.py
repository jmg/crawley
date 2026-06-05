"""INI based configuration for DSL projects."""

import os.path
from configparser import ConfigParser


class ConfigObj:
    """A dictionary view of ``(section, item)`` over an INI file."""

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
            value = ""
        self.config[key] = value
        section, item = key
        if not self._config_parser.has_section(section):
            self._config_parser.add_section(section)
        self._config_parser.set(section, item, value)

    def __str__(self):
        return str(self.config)

    def save(self, filename):
        with open(filename, "w") as f:
            self._config_parser.write(f)


class ConfigApp(ConfigObj):
    """Read ``config.ini`` from a directory and expose it as a dict."""

    CONFIG_FILE = "config.ini"

    def __init__(self, ini_dir):
        super().__init__()
        self.ini_dir = ini_dir
        with open(self._get_path(), "r") as f:
            self._config_parser.read_file(f)
        self._update_dictionary()

    def _get_path(self):
        return os.path.join(self.ini_dir, self.CONFIG_FILE)

    def save(self):
        ConfigObj.save(self, self._get_path())
