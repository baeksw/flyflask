import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="flykoma",
    version="0.0.1",
    author="SeungWoo.BAEK",
    author_email="dohaskell7@gmail.com",
    description=("Utility"),
    license="BSD",
    keywords="koma project",
    url="http://packages.python.org/koma_project",
    packages=['flykoma','flykoma.templates', 'flykoma.static'],
    package_data={
        'flykoma': ['*'],  # All files from folder A
        'flykoma.static': ['*'],  # All files from folder A
        'flykoma.templates': ['*', '*.html', '*.tpl'],  # All files from folder A
        '' : [ '*.html', '*.xml', '*.json' , '*.txt']
    },
    
#     include_package_data=True,
    long_description=read('README'),
    install_requires=['Flask','flask-bootstrap']
)
        