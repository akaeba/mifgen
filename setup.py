# -*- coding: utf-8 -*-
"""
@author:        Andreas Kaeberlein
@copyright:     Copyright 2024
@credits:       AKAE

@license:       GPLv3
@maintainer:    Andreas Kaeberlein
@email:         andreas.kaeberlein@web.de

@file:          setup.py
@date:          2024-01-13

@note           setup pip installer
"""



#------------------------------------------------------------------------------
# Python Libs
#
import setuptools
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='mifgen',
    version='0.1.0',
    scripts=['mifgen'],
    install_requires = [],
    author='Andreas Kaeberlein',
    author_email="andreas.kaeberlein@web.de",
    license="GPLv3",
    platforms="Any",
    description="Converter to Altera MIF file format.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/akaeba/mifgen",
    download_url = "https://pypi.org/project/mifgen",
    packages=["mifgen"],	# define package to add
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
#------------------------------------------------------------------------------
