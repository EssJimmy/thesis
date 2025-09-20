from setuptools import setup, find_packages
from version import __version__

setup(
    name='grpc_cv_service',
    version=__version__,
    author='Jimmy',
    packages=find_packages(),
)