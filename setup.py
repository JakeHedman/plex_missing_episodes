#coding: utf-8
from setuptools import setup

setup(
    version='0.1',
    name = "plex_missing_episodes",
    packages = ['plex_missing_episodes'],
    description='Torrent RSS downloader',
    author='Oskar Hallström',
    author_email='ooskar@ooskar.com',
    maintainer='Jakob Hedman',
    maintainer_email='jakob@hedman.email',
    license='GNU GPLv3',
    url='https://github.com/spillevink/plex_missing_episodes',
    package_dir = {'plex_missing_episodes':'plex_missing_episodes'},
    entry_points = {
        'console_scripts': [
            'plex_missing_episodes = plex_missing_episodes.plex_missing_episodes:main.command',
        ],
    },
    install_requires = [
        'opster',
        'tvdb_api',
        'plexapi',
    ],
    long_description = open('README.rst').read(),
)
