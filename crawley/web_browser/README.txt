**************************************************************
                  SimpleWebBrowser v1.0
**************************************************************

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


**************************************************************
                        Short Cuts
**************************************************************

- Crtl + r / F5 = Reload
- Crtl + t = New tab
- Alt + left arrow = go-back
- Alt + right arrow = go-ahead


**************************************************************
                       Dependencies
**************************************************************

- python
- python-qt4

**************************************************************





