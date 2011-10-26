import os.path
from PyQt4 import QtGui, QtWebKit
from PyQt4.uic import loadUi
from base import Ui_MainWindow
from config import Ui_FrmConfig
from settings import Ui_Settings

PATH = os.path.dirname(os.path.abspath(__file__))

class BrowserGUI(QtGui.QMainWindow):
    """
        The Graphical user interface of the browser
    """

    def __init__(self):

        QtGui.QMainWindow.__init__(self)
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)                  

        self.ui.bt_back.setIcon(QtGui.QIcon().fromTheme("go-previous"))
        self.ui.bt_ahead.setIcon(QtGui.QIcon().fromTheme("go-next"))
        self.ui.bt_reload.setIcon(QtGui.QIcon().fromTheme("view-refresh"))

        self.setWindowIcon(QtGui.QIcon("GUI/logo.png"))

        self.ui.tab_pages.setCornerWidget(QtGui.QToolButton(self, text="New Tab", icon=QtGui.QIcon.fromTheme("document-new"), clicked=self.add_tab, shortcut="Ctrl+t"))


class BrowserTabGUI(QtGui.QTabWidget):
    """
        The Graphical user interface of the browser tabs
    """

    def __init__(self, parent):

        QtGui.QTabWidget.__init__(self)

        self.pg_load = QtGui.QProgressBar(maximumWidth=200, visible=False)
        self.html = QtWebKit.QWebView(parent.tab_pages.currentWidget())
        self.parent = parent

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.html)
        layout.addWidget(self.pg_load)
        self.setLayout(layout)


class FrmConfigGUI(QtGui.QDialog):

    def __init__(self, parent):
        
        QtGui.QDialog.__init__(self, parent)
        
        self.config_ui = Ui_FrmConfig()
        self.config_ui.setupUi(self)
        
        
class FrmSettingsGUI(QtGui.QDialog):

    def __init__(self, parent):
        
        QtGui.QDialog.__init__(self, parent)
        
        self.settings_ui = Ui_Settings()
        self.settings_ui.setupUi(self)

