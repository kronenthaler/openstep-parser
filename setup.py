from setuptools import setup, find_packages


setup(name='openstep_parser',
    author='Ignacio Calderon',
    description='OpenStep plist reader into python objects',
    url="http://github.com/kronenthaler/openstep-parser",
    version='1.2',
    license='BSD License',
    packages=find_packages(exclude=['tests']))
