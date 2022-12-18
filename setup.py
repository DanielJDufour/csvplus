from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
  name = 'csvplus',
  packages = ['csvplus'],
  package_dir = {'csvplus': 'csvplus'},
  package_data = {'csvplus': ['__init__.py']},
  version = '0.0.1',
  description = 'Create, Read, Update, Delete, and Move Rows in a CSV File',
  long_description = long_description,
  long_description_content_type='text/markdown',
  author = 'Daniel J. Dufour',
  author_email = 'daniel.j.dufour@gmail.com',
  url = 'https://github.com/DanielJDufour/csvplus',
  download_url = 'https://github.com/DanielJDufour/csvplus/tarball/download',
  keywords = ['create', 'crud', 'csv', 'delete', 'move', 'read', 'update'],
  classifiers = [
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent'
  ],
  install_requires=[]
)
