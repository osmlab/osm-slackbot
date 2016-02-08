#!/usr/bin/env python

from setuptools import setup

setup(
    name='osm-slackbot',
    version='0.0.2',
    install_requires=[],
    author='pjdufour',
    author_email='pjdufour.dev@gmail.com',
    license='BSD License',
    url='https://github.com/pjdufour/osm-slackbot/',
    keywords='python gis slack osm',
    description='Slack Bot for OpenStreetMap',
    long_description=open('README.rst').read(),
    download_url="https://github.com/pjdufour/osm-slackbot/zipball/master",
    packages=[
        "osmslackbot",
        "osmslackbot.broker",
        "osmslackbot.mapping",
        "osmslackbot.tests"],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
