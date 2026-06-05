"""
    Graphical user interface widgets for the crawley browser.

    Glues together the Qt Designer generated forms (``base``, ``config`` and
    ``settings``) into ready to use PySide6 widgets.
"""

import os.path

from PySide6 import QtGui, QtWebEngineWidgets, QtWidgets

from crawley.web_browser.GUI.base import Ui_MainWindow
from crawley.web_browser.GUI.config import Ui_FrmConfig
from crawley.web_browser.GUI.settings import Ui_Settings

PATH = os.path.dirname(os.path.abspath(__file__))


class BrowserGUI(QtWidgets.QMainWindow):
    """
        The Graphical user interface of the browser.
    """

    def __init__(self):

        QtWidgets.QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.bt_back.setIcon(QtGui.QIcon.fromTheme("go-previous"))
        self.ui.bt_ahead.setIcon(QtGui.QIcon.fromTheme("go-next"))
        self.ui.bt_reload.setIcon(QtGui.QIcon.fromTheme("view-refresh"))

        self.setWindowIcon(QtGui.QIcon(os.path.join(PATH, "logo.png")))

        self.ui.tab_pages.setCornerWidget(
            QtWidgets.QToolButton(
                self,
                text="New Tab",
                icon=QtGui.QIcon.fromTheme("document-new"),
                clicked=self.add_tab,
                shortcut="Ctrl+t",
            )
        )


class BrowserTabGUI(QtWidgets.QTabWidget):
    """
        The Graphical user interface of the browser tabs.
    """

    def __init__(self, parent):

        QtWidgets.QTabWidget.__init__(self)

        self.pg_load = QtWidgets.QProgressBar(maximumWidth=200, visible=False)
        self.html = QtWebEngineWidgets.QWebEngineView(parent.tab_pages.currentWidget())
        self.parent = parent

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.html)
        layout.addWidget(self.pg_load)
        self.setLayout(layout)


class FrmConfigGUI(QtWidgets.QDialog):

    def __init__(self, parent):

        QtWidgets.QDialog.__init__(self, parent)

        self.config_ui = Ui_FrmConfig()
        self.config_ui.setupUi(self)


class FrmSettingsGUI(QtWidgets.QDialog):

    def __init__(self, parent):

        QtWidgets.QDialog.__init__(self, parent)

        self.settings_ui = Ui_Settings()
        self.settings_ui.setupUi(self)
