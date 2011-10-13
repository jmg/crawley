#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

templates_dir = os.path.join("crawley", "conf", "templates")
templates_files = [os.path.join(templates_dir, file) for file in os.listdir(templates_dir)]

setup(
    name="crawley",
    version="0.0.6",
    description="Pythonic Scraping / Crawling FrameWork built On Eventlet",
    author="Crawley Developers",
    author_email = "jmg.utn@gmail.com",
    license = "GPL v3",
    keywords = "Scraping Crawling Framework Python",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),      
    data_files=[
        ('crawley/conf/templates', templates_files)
    ],
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
