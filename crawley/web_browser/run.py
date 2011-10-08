"""
    ****************** SimpleWebBrowser v1.0 *********************

    A Simple Fully Functional Web Browser implemented over Qt
    and QtWebKit.

    This browser have the basic functions of a clasic web browser
    and it's thought to be easily extended and maintainable.

    It separates the GUI from the logic from the implementation in
    many classes. The inheritance hierarchy looks like this:

        BrowserGUI -> BrowserBase -> Browser
        BrowserTabGUI -> BrowserTabBase -> BrowserTab

        [GUI -> Logic Definition -> Logic Implementation]

    If you have any commentary, query or bug report you can contact
    me to my mail.

    To run this program just type:

        ~$ python run.py

    Inside the main directory.

    author: Juan Manuel Garcia <jmg.utn@gmail.com>
"""

import sys
from PyQt4 import QtGui
from browser import Browser

if __name__ == "__main__":
    """ Run the browser """

    app = QtGui.QApplication(sys.argv)
    main = Browser()
    main.show()
    sys.exit(app.exec_())
