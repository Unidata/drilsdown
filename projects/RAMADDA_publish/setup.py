from setuptools import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
 

setup( 
    name='ramadda_publish',
    version='1.3',
    url="https://github.com/suvarchal/RAMADDA_publish",
    author='Suvarchal',
    author_email='suvarchal.kumar@gmail.com',
    license="MIT",
    description="python script to make automated entries to ramadda",
    #long_description=read('README.md'),
    scripts=['bin/ramadda_publish'],
    classifiers=[
    'Development Status :: 4 - Beta',

    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
]
)

