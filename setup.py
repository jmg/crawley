#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="crawley",
    version="0.0.6",
    description="Pythonic Scraping / Crawling FrameWork built On Eventlet",
    author="Crawley Developers",
    author_email = "jmg.utn@gmail.com",
    license = "GPL v3",
    keywords = "Scraping Crawling Framework Python",    
    packages=['crawley', 'crawley.manager', 'crawley.persistance', 'crawley.persistance.documents', 'crawley.manager.commands', 'crawley.http', 'crawley.conf.project_template', 
              'crawley.web_browser', 'crawley.web_browser.GUI'],
    scripts=['crawley/bin/crawley'],
    install_requires=[
        'lxml',
        'eventlet',
        'elixir',
        'pyquery',
    ],
    url='https://github.com/jmg/crawley',
)
