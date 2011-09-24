#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from crawley import __version__

setup(
    name="crawley",
    version=__version__,
    description="Pythonic Scraping / Crawling FrameWork built On Eventlet",
    author="Crawley Developers",
    author_email = "jmg.utn@gmail.com",
    license = "GPL v3",
    keywords = "Scraping Crawling Framework Python",    
    packages=['crawley', 'crawley.manager', 'crawley.manager.commands', 'crawley.conf.project_template'],
    scripts=['crawley/bin/crawley'],
    url='https://github.com/jmg/crawley',
)
