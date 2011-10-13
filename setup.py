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
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_data={
      'templates': ['crawley/conf/templates/*.tm'],
    },
    include_package_data=True,    
    scripts=['crawley/bin/crawley'],    
    install_requires=[
        'lxml',
        'eventlet',
        'elixir',
        'pyquery',        
    ],
    url='http://crawley-project.com.ar/',
)
