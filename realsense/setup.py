from setuptools import  setup, find_packages
from version import __version__

setup(
    name='realsense',
    version=__version__,
    author='Jimmy',
    packages=find_packages(),
)