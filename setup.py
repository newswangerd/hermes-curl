from setuptools import setup, find_packages

setup(
    name='hermes_curl',
    version='1.0.0',
    entry_points={
        'console_scripts': ['hermes=hermes.main:main'],
    },
    install_requires=[
        'PyYAML==5.4.1'
    ],
    packages=find_packages(exclude=["tests", "tests.*"]),
)
