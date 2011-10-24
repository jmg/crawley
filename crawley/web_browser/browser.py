import multiprocessing

from lxml import etree
from PyQt4 import QtCore, QtWebKit, QtGui
from baseBrowser import BaseBrowser, BaseBrowserTab, FrmBaseConfig
from config import DEFAULTS, SELECTED_CLASS

from crawley.crawlers.offline import OffLineCrawler
from crawley.manager.utils import get_full_template_path
from crawley.exceptions import InvalidProjectError        
from crawley.extractors import XPathExtractor
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

    def load_url(self, url, selected_nodes=None):
        """ 
            Load the requested url in the webwiew
        """

        self.url = str(url)
        html = self.crawler._get_data(self.url)

        with open(get_full_template_path("html_template"), "r") as f:
            template = f.read()
            html = template % {'content': html, 'css_class': SELECTED_CLASS }
            
        if selected_nodes is not None:
            html = self._highlight_nodes(html, selected_nodes)

        self.html.setHtml(html)
        self.html.show()
        
    def _highlight_nodes(self, html, nodes):
        """
            Highlights the nodes selected by the user in the current page
        """
        
        html_tree = XPathExtractor().get_object(html)
        
        for xpath in nodes:
            
            tags = html_tree.xpath(xpath)
            
            if tags:
            
                tag = tags[0]
                
                classes = tag.attrib.get("class", "")
                classes = "%s %s" % (classes, SELECTED_CLASS)
                tag.attrib["class"] = classes.strip()
                tag.attrib["id"] = xpath
        
        return etree.tostring(html_tree.getroot(), pretty_print=True, method="html")

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
            dir_name = str(QtGui.QFileDialog.getSaveFileName(self, 'Start Project'))
            
        if not dir_name:
            return
            
        try:        
            self.current_project = GUIProject(dir_name)
            self.current_project.set_up(self, is_new)
                    
            self._disable_enable_project_buttons(True)
            
            if is_new:
                self.configure()
        
        except InvalidProjectError, e:
            
            print "%s" % e
            
            self._disable_enable_project_buttons(False)
            
    def configure(self):
        """
            Configure a project accesing the config.ini file
        """
        
        frm_config = FrmConfig(self, self.current_project)
        frm_config.show()                
    
    def save(self):
        """
            Saves a crawley project
        """
        
        self.generate()
    
    def generate(self):
        """
            Generates a DSL template 
        """
        
        if self.is_current():
            
            url = self.parent.tb_url.text()

            main_frame = self.html.page().mainFrame()
            content = unicode(main_frame.toHtml())
            self.current_project.generate_template(url, content)
            
    def _run(self):
        """
            Run the crawler in other process
        """
        self.generate()
        
        self.current_project.run()
        self._disable_enable_buttons(True)

    def run(self):
        """
            Runs the current project
        """
                
        self._disable_enable_buttons(False, also_run=False)
        self._change_run_handler(self.run, self.stop, "Stop Crawler")
        
        self.process = multiprocessing.Process(target=self._run)
        self.process.start()
    
    def _change_run_handler(self, curr_handler, new_handler, label):
        """
            Connects the run signal to another handler
        """
        
        self.disconnect(self.parent.bt_run, QtCore.SIGNAL("clicked()"), curr_handler)
        self.connect(self.parent.bt_run, QtCore.SIGNAL("clicked()"), new_handler)
        
        self.parent.bt_run.setText(label)
    
    def stop(self):
        """
            Kills the running crawler process
        """
        
        self.process.terminate()
        self._change_run_handler(self.stop, self.run, "Run Crawler")
        self._disable_enable_buttons(True)

    def is_current(self):
        """" 
            Return true if this is the current active tab 
        """
        
        return self is self.parent.tab_pages.currentWidget()
        
    def _disable_enable_buttons(self, enable, also_run=True):
        """
            Disables crawley related buttons 
            enable: boolean
        """
                
        self.parent.bt_configure.setEnabled(enable)        
        self.parent.bt_start.setEnabled(enable)
        self.parent.bt_open.setEnabled(enable)
        self.parent.bt_save.setEnabled(enable)
        
        if also_run:
            self.parent.bt_run.setEnabled(enable)
        
    def _disable_enable_project_buttons(self, enable):
        """
            Disables crawley project related buttons 
            enable: boolean
        """
                
        self.parent.bt_configure.setEnabled(enable)
        self.parent.bt_run.setEnabled(enable) 
        self.parent.bt_save.setEnabled(enable)


class FrmConfig(FrmBaseConfig):
    """
        A GUI on the top of the config.ini files of crawley projects.
    """
    
    INFINITE = "Infinite"
    MAX_DEPTH_OPTIONS = 100
    
    def __init__(self, parent, current_project):
        """
            Setups the frm config window
        """
        
        FrmBaseConfig.__init__(self, parent)
        self.current_project = current_project
        
        self.config = current_project.get_configuration()
        self.config_ui.tb_start_url.setText(self.config[("crawler", "start_urls")])        
        
        items = ["%s" % i for i in range(self.MAX_DEPTH_OPTIONS)]
        items.append(self.INFINITE)
        
        self.config_ui.cb_max_depth.addItems(items)
        
        max_depth = int(self.config[("crawler", "max_depth")])
        max_depth = self._check_infinite(max_depth, infinite_value=-1, get_index=True)
        
        self.config_ui.cb_max_depth.setCurrentIndex(max_depth)
        
    def _check_infinite(self, max_depth, infinite_value=INFINITE, get_index=False):
        """
            Check if max_depth is infinite or not
        """
        
        if max_depth == infinite_value:
            if get_index:
                return self.MAX_DEPTH_OPTIONS
            return -1
        return max_depth
    
    def ok(self):
        """
            Gets the new config file
        """
        
        max_depth = self.config_ui.cb_max_depth.currentText()
        max_depth = self._check_infinite(max_depth)
        self.config[("crawler", "max_depth")] = max_depth
        
        start_url = self.config_ui.tb_start_url.text()                
        self.config[("crawler", "start_urls")] = start_url
        
        self.config.save()
        self.close()
        
    def cancel(self):
        """
            Closes the dialog
        """
        self.close()
