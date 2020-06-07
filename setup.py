from setuptools import setup, find_packages
from os import path


here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='vexing_gopher',
      version='0.0.1',
      description='Gopher server for DEFCONMeshnet',
      long_description=long_description,
      author='signal9',
      packages=find_packages(exclude=['tests']),
      include_package_data=True,
      package_data={
          'vexing_gopher': ['templates/*.gopher']
      },
      entry_points={
          'console_scripts': [
              'vexing_gopher = vexing_gopher.run_server:main'
          ]
      },
      install_requires=[
          'flask~=1.1.2',
          'flask-gopher~=2.2.1'
      ])
