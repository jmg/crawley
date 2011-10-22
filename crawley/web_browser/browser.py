import threading

from PyQt4 import QtCore, QtWebKit, QtGui
from baseBrowser import BaseBrowser, BaseBrowserTab, FrmBaseConfig
from config import DEFAULTS, SELECTED_CLASS

from crawley.crawlers.offline import OffLineCrawler
from crawley.manager.utils import get_full_template_path
from gui_project import GUIProject

class Browser(BaseBrowser):
    """
        A Browser representation

        This class overrides all the methods of the
        base class.
    """

    def __init__(self, default_url=None):

        if default_url is None:
            default_url = DEFAULTS['url']

        self.default_url = default_url
        BaseBrowser.__init__(self)
        self.add_tab()

    def current_tab(self):
        """
            Return the current tab
        """

        return self.ui.tab_pages.currentWidget()

    def browse(self):
        """
            Make a browse and call the url loader method
        """

        url = self.ui.tb_url.text() if self.ui.tb_url.text() else self.default_url
        if not DEFAULTS['protocol'] in url:
            url = "%s://%s" % (DEFAULTS['protocol'], url)
        tab = self.current_tab()
        self.ui.tb_url.setText(url)
        tab.load_url(url)

    def add_tab(self):
        """
            Add a new tab to the browser
        """

        index = self.ui.tab_pages.addTab(BrowserTab(self.ui), "New Tab")
        self.ui.tab_pages.setCurrentIndex(index)
        self.ui.tb_url.setFocus()
        self.browse()

    def tab_closed(self, index):
        """
            Triggered when the user close a tab
        """

        self.ui.tab_pages.widget(index).deleteLater()
        if self.ui.tab_pages.count() <= 1:
            self.close()

    def tab_changed(self, index):
        """
            Triggered when the current tab changes
        """

        tab = self.current_tab()
        if tab is not None and tab.url is not None:
            self.ui.tb_url.setText(tab.url)

    def show(self):
        """
            Show the main windows
        """

        BaseBrowser.show(self)


class BrowserTab(BaseBrowserTab):
    """
        A Browser Tab representation

        This class overrides all the methods of the
        base class.
    """

    def __init__(self, parent):

        BaseBrowserTab.__init__(self, parent)
        self.url = None
        self.crawler = OffLineCrawler()

    def load_bar(self, value):
        """
            Load the progress bar
        """

        self.pg_load.setValue(value)

    def loaded_bar(self, state):
        """
            Triggered when the bar finish the loading
        """

        self.pg_load.hide()
        index = self.parent.tab_pages.indexOf(self)
        self.parent.tab_pages.setTabText(index, self.html.title())
        self.parent.tab_pages.setTabIcon(index, QtWebKit.QWebSettings.iconForUrl(QtCore.QUrl(self.url)))

    def load_start(self):
        """
            Show the progress bar
        """

        self.pg_load.show()

    def load_url(self, url):
        """
            Load the requested url in the webwiew
        """

        self.url = str(url)
        html = self.crawler._get_data(self.url)

        with open(get_full_template_path("html_template"), "r") as f:
            template = f.read()
            html = template % {'content': html, 'css_class': SELECTED_CLASS }

        self.html.setHtml(html)
        self.html.show()

    def url_changed(self, url):
        """
            Update the url text box
        """

        if self.is_current():
            self.parent.tb_url.setText(self.url)
        self.url = url.toString()

    def back(self):
        """
            Back to previous page
        """

        if self.is_current():
            self.html.back()

    def ahead(self):
        """
            Go to next page
        """

        if self.is_current():
            self.html.forward()

    def reload(self):
        """
            Reload page
        """

        if self.is_current():
            self.html.reload()

    def start(self):
        """
            Starts a new project
        """

        self._start(is_new=True)

    def open(self):
        """
            Opens an existing project
        """

        self._start()

    def _start(self, is_new=False):
        """
            starts or opens a project depending on
            [is_new] parameter
        """

        if not is_new:
            dir_name = str(QtGui.QFileDialog.getExistingDirectory(self, 'Open Project'))
        else:
            dir_name = str(QtGui.QFileDialog.getSaveFileName(self, 'Project Name'))

        url = str(self.parent.tb_url.text())
        self.current_project = GUIProject(dir_name, url)

        self.current_project.set_up(is_new)

        self.parent.bt_run.setEnabled(True)
        self.parent.bt_generate.setEnabled(True)
        self.parent.bt_configure.setEnabled(True)

    def configure(self):
        """
            Configure a project accesing the config.ini file
        """

        frm_config = FrmConfig(self, self.current_project)
        frm_config.show()

    def generate(self):
        """
            Generates a DSL template
        """

        if self.is_current():

            main_frame = self.html.page().mainFrame()
            content = unicode(main_frame.toHtml())
            self.current_project.generate_template(content)

    def _run(self):
        """
            Run the crawler in other thread
        """

        self.current_project.run()
        self._disable_enable_buttons(True)

    def run(self):
        """
            Runs the current project
        """

        self._disable_enable_buttons(False)

        t = threading.Thread(target=self._run)
        t.start()

    def is_current(self):
        """"
            Return true if this is the current active tab
        """

        return self is self.parent.tab_pages.currentWidget()

    def _disable_enable_buttons(self, enable):
        """
            Disables crawley related buttons
            enable: boolean
        """

        self.parent.bt_generate.setEnabled(enable)
        self.parent.bt_configure.setEnabled(enable)
        self.parent.bt_run.setEnabled(enable)
        self.parent.bt_start.setEnabled(enable)
        self.parent.bt_open.setEnabled(enable)


class FrmConfig(FrmBaseConfig):

    def __init__(self, parent, current_project):

        FrmBaseConfig.__init__(self, parent)
        self.current_project = current_project
        self.config_ui.tb_config.setPlainText(current_project.get_configuration())

    def ok(self):
        """
            Gets the new config file
        """
        config = self.config_ui.tb_config.toPlainText()
        self.current_project.save_config(config)
        self.close()

    def cancel(self):
        """
            Closes the dialog
        """
        self.close()
