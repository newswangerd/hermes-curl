from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='hermes_curl',
    version='1.0.3',
    entry_points={
        'console_scripts': ['hermes=hermes.main:main'],
    },
    install_requires=[
        'PyYAML==5.4.1'
    ],
    packages=find_packages(exclude=["tests", "tests.*"]),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/newswangerd/hermes-curl',
    description='Hermes cURL is a lightweight wrapper on top of cURL that' +
        ' provides reusable HTTP request configurations in YAML.'
)
