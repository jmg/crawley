"""
    Crawley web browser package.

    A PySide6 + QtWebEngine GUI used to visually build crawley projects.

    Nothing is imported eagerly here so that importing ``crawley`` (or
    ``crawley.manager``) never pulls in PySide6. The browser is meant to be
    imported lazily, e.g. ``from crawley.web_browser.browser import Browser``.
"""
