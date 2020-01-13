from setuptools import setup, find_packages


def find_version(*file_paths):
    def read(*parts):
        import codecs
        import os
        here = os.path.abspath(os.path.dirname(__file__))
        with codecs.open(os.path.join(here, *parts), 'r') as fp:
            return fp.read()

    import re
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='openstep_parser',
    author='Ignacio Calderon',
    description='OpenStep plist reader into python objects',
    url="http://github.com/kronenthaler/openstep-parser",
    version=find_version("openstep_parser", "__init__.py"),
    license='BSD License',
    packages=find_packages(exclude=['tests'])
)
