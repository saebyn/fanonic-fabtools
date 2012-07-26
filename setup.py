"""
distutils setup.py file.

"""

from distutils.core import setup

setup(
    name = 'fabtools',
    version = '0.0.1',
    description = 'Handy tasks for fabric',

    long_description = open('README.rst').read(),
    packages = ['fabtools'],

    maintainer = 'John Weaver',
    maintainer_email = 'john@saebyn.info',
)
