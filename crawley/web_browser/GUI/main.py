import os.path
from PyQt4 import QtGui, QtWebKit
from PyQt4.uic import loadUi

class BrowserGUI(QtGui.QMainWindow):
    """
        The Graphical user interface of the browser
    """

    def __init__(self):

        QtGui.QMainWindow.__init__(self)
        self.ui = loadUi(os.path.join(os.getcwd(), "crawley", "web_browser", "GUI", "main.ui"))

        self.ui.bt_back.setIcon(QtGui.QIcon().fromTheme("go-previous"))
        self.ui.bt_ahead.setIcon(QtGui.QIcon().fromTheme("go-next"))
        self.ui.bt_reload.setIcon(QtGui.QIcon().fromTheme("view-refresh"))

        self.ui.setWindowIcon(QtGui.QIcon("GUI/logo.png"))

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



