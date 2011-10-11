import os

from PyQt4 import QtCore, QtWebKit
from baseBrowser import BaseBrowser, BaseBrowserTab
from config import DEFAULTS, SELECTED_CLASS
from crawley.crawlers.fast import FastCrawler
from crawley.extractors import PyQueryExtractor

PATH = os.path.dirname(os.path.abspath(__file__))

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
        """ Return the current tab """
        return self.ui.tab_pages.currentWidget()

    def browse(self):
        """ Make a browse and call the url loader method """
        url = self.ui.tb_url.text() if self.ui.tb_url.text() else self.default_url
        if not DEFAULTS['protocol'] in url:
            url = "%s://%s" % (DEFAULTS['protocol'], url)
        tab = self.current_tab()
        self.ui.tb_url.setText(url)
        tab.load_url(url)

    def add_tab(self):
        """ Add a new tab to the browser """
        index = self.ui.tab_pages.addTab(BrowserTab(self.ui), "New Tab")
        self.ui.tab_pages.setCurrentIndex(index)
        self.ui.tb_url.setFocus()
        self.browse()

    def tab_closed(self, index):
        """ Triggered when the user close a tab """
        self.ui.tab_pages.widget(index).deleteLater()
        if self.ui.tab_pages.count() <= 1:
            self.close()

    def tab_changed(self, index):
        """ Triggered when the current tab changes """
        tab = self.current_tab()
        if tab is not None and tab.url is not None:
            self.ui.tb_url.setText(tab.url)

    def show(self):
        """ Show the main windows """
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
        self.crawler = FastCrawler()

    def load_bar(self, value):
        """ Load the progress bar """
        self.pg_load.setValue(value)

    def loaded_bar(self, state):
        """ Triggered when the bar finish the loading """
        self.pg_load.hide()
        index = self.parent.tab_pages.indexOf(self)
        self.parent.tab_pages.setTabText(index, self.html.title())
        self.parent.tab_pages.setTabIcon(index, QtWebKit.QWebSettings.iconForUrl(QtCore.QUrl(self.url)))

    def load_start(self):
        """ Show the progress bar """
        self.pg_load.show()

    def load_url(self, url):
        """ Load the requested url in the webwiew """        
        
        self.url = str(url)
        html = self.crawler._get_data(self.url)
        
        with open(os.path.join(PATH, "template.py"), "r") as f:
            template = f.read()
            html = template % {'content': html, 'css_class': SELECTED_CLASS }
                
        self.html.setHtml(html)
        self.html.show()

    def url_changed(self, url):
        """ Update the url text box """
        if self.is_current():
            self.parent.tb_url.setText(self.url)
        self.url = url.toString()
        #self.load_url(self.url)

    def back(self):
        """" Back to previous page """
        if self.is_current():
            self.html.back()

    def ahead(self):
        """" Go to next page """
        if self.is_current():
            self.html.forward()

    def reload(self):
        """" Reload page """
        if self.is_current():
            self.html.reload()
            
    def generate(self):
        """" generate template """
        if self.is_current():
            main_frame = self.html.page().mainFrame()
            content = unicode(main_frame.toHtml())
            
            obj = PyQueryExtractor().get_object(content)
            elements = obj(".%s" % SELECTED_CLASS)        
            
            elements_xpath = [e.get("id") for e in elements]
            
            stream = ""                        
            for i, e in enumerate(elements_xpath):                
                stream += "%s -> %s <br/>" % ("my_field_%s" % i, e)                            
            
            self.html.setHtml(stream)
            self.html.show()
            

    def is_current(self):
        """" Return true if this is the current active tab """
        return self is self.parent.tab_pages.currentWidget()
