from PyQt4 import QtCore, QtWebKit, QtGui
from GUI import BrowserGUI, BrowserTabGUI

actions = {"Alt+Left" : QtWebKit.QWebPage.Back, "Alt+Right" : QtWebKit.QWebPage.Forward, "F5" : QtWebKit.QWebPage.Reload }

class BaseBrowser(BrowserGUI):
    """
        This class is the base for a simple web browser

        Inherit from this class and override all the virtual methods
        to make a full functional browser
    """

    def __init__(self):

        BrowserGUI.__init__(self)

        self.connect(self.ui.tb_url, QtCore.SIGNAL("returnPressed()"), self.browse)
        self.connect(self.ui.tab_pages, QtCore.SIGNAL("tabCloseRequested(int)"), self.tab_closed)
        self.connect(self.ui.tab_pages, QtCore.SIGNAL("currentChanged(int)"), self.tab_changed)

    # overridable methods section

    def browse():
        pass

    def tab_closed(index):
        pass

    def tab_changed(index):
        pass

    def add_tab():
        pass


class BaseBrowserTab(BrowserTabGUI):
    """
        This class is the base for a browser tab

        Inherit from this class and override all the virtual methods
        to make a browser tab
    """

    def __init__(self, parent):

        BrowserTabGUI.__init__(self, parent)

        self.connect(self.parent.bt_back, QtCore.SIGNAL("clicked()"), self.back)
        self.connect(self.parent.bt_ahead, QtCore.SIGNAL("clicked()"), self.ahead)
        self.connect(self.parent.bt_reload, QtCore.SIGNAL("clicked()"), self.reload)
        self.connect(self.parent.bt_generate, QtCore.SIGNAL("clicked()"), self.generate)
        self.connect(self.parent.bt_run, QtCore.SIGNAL("clicked()"), self.run)
        self.connect(self.parent.bt_start, QtCore.SIGNAL("clicked()"), self.start)
        
        self.connect(self.html, QtCore.SIGNAL("loadStarted()"), self.load_start)
        self.connect(self.html, QtCore.SIGNAL("loadFinished(bool)"), self.loaded_bar)
        self.connect(self.html, QtCore.SIGNAL("loadProgress(int)"), self.load_bar)
        self.connect(self.html, QtCore.SIGNAL("urlChanged(const QUrl)"), self.url_changed)


    # overridable methods section

    def load_start(self):
        pass

    def load_bar(self):
        pass

    def loaded_bar(self):
        pass

    def url_changed(self):
        pass

    def back(self):
        pass

    def ahead(self):
        pass

    def reload():
        pass

