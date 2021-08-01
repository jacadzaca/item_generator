from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='wow item creator',
    version='0.1.0',
    description='a simple script that generates random items from description',
    long_description=readme,
    author='jacadzaca',
    author_email='vitouejj@gmail.com',
    url='https://github.com/jacadzaca/item_creator',
    license=license,
    packages=find_packages(exclude=('tests', 'docs', 'venv', 'templates'))
)
