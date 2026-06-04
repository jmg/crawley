"""
    Base browser definitions.

    Defines the logic layer base classes that sit between the Qt Designer
    generated GUI classes and the concrete browser implementation. These
    classes wire up the Qt signals and declare the overridable handlers.
"""

from PySide6.QtWebEngineCore import QWebEnginePage

from crawley.web_browser.GUI import (
    BrowserGUI,
    BrowserTabGUI,
    FrmConfigGUI,
    FrmSettingsGUI,
)

actions = {
    "Alt+Left": QWebEnginePage.WebAction.Back,
    "Alt+Right": QWebEnginePage.WebAction.Forward,
    "F5": QWebEnginePage.WebAction.Reload,
}


class BaseBrowser(BrowserGUI):
    """
        This class is the base for a simple web browser

        Inherit from this class and override all the virtual methods
        to make a full functional browser
    """

    def __init__(self):

        BrowserGUI.__init__(self)

        self.ui.tb_url.returnPressed.connect(self.browse)
        self.ui.tab_pages.tabCloseRequested.connect(self.tab_closed)
        self.ui.tab_pages.currentChanged.connect(self.tab_changed)

    # overridable methods section

    def browse(self):
        pass

    def tab_closed(self, index):
        pass

    def tab_changed(self, index):
        pass

    def add_tab(self):
        pass


class BaseBrowserTab(BrowserTabGUI):
    """
        This class is the base for a browser tab

        Inherit from this class and override all the virtual methods
        to make a browser tab
    """

    def __init__(self, parent):

        BrowserTabGUI.__init__(self, parent)

        self.parent.bt_back.clicked.connect(self.back)
        self.parent.bt_ahead.clicked.connect(self.ahead)
        self.parent.bt_reload.clicked.connect(self.reload)
        self.parent.bt_save.clicked.connect(self.save)
        self.parent.bt_run.clicked.connect(self.run)
        self.parent.bt_start.clicked.connect(self.start)
        self.parent.bt_open.clicked.connect(self.open)
        self.parent.bt_configure.clicked.connect(self.configure)
        self.parent.bt_settings.clicked.connect(self.settings)

        self.html.loadStarted.connect(self.load_start)
        self.html.loadFinished.connect(self.loaded_bar)
        self.html.loadProgress.connect(self.load_bar)
        self.html.urlChanged.connect(self.url_changed)

        self._disable_enable_project_buttons(False)

    # overridable methods section

    def load_start(self):
        pass

    def load_bar(self, value):
        pass

    def loaded_bar(self, state):
        pass

    def url_changed(self, url):
        pass

    def back(self):
        pass

    def ahead(self):
        pass

    def reload(self):
        pass


class FrmBaseConfig(FrmConfigGUI):

    def __init__(self, parent):

        FrmConfigGUI.__init__(self, parent)
        self.config_ui.bt_ok.clicked.connect(self.ok)
        self.config_ui.bt_cancel.clicked.connect(self.cancel)


class FrmBaseSettings(FrmSettingsGUI):

    def __init__(self, parent):

        FrmSettingsGUI.__init__(self, parent)
        self.settings_ui.bt_ok.clicked.connect(self.ok)
        self.settings_ui.bt_cancel.clicked.connect(self.cancel)
