from setuptools import setup, find_packages

setup(name='hermes_curl',
      version='0.0.1',
      entry_points = {
        'console_scripts': ['hermes=hermes.main:main'],
    }
)
