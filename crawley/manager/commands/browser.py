"""``browser`` command: launch the (optional) PySide6 scraping browser."""

import sys

from crawley.manager.commands.command import BaseCommand
from crawley.utils import exit_with_error


class BrowserCommand(BaseCommand):
    """Open the visual scraping browser on the given url."""

    name = "browser"

    def validations(self):
        return [(len(self.args) >= 1, "No given url")]

    def execute(self):
        try:
            from PySide6 import QtWidgets

            from crawley.web_browser.browser import Browser
        except ImportError:
            exit_with_error(
                "The browser requires PySide6. Install it with: "
                "pip install 'crawley[gui]'"
            )
            return

        app = QtWidgets.QApplication(sys.argv)
        main = Browser(self.args[0])
        main.show()
        sys.exit(app.exec())
