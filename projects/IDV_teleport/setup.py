from setuptools import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
 

setup( 
    name='idv_teleport',
    version='1.6',
    url="https://github.com/suvarchal/IDV_teleport",
    author='Suvarchal',
    author_email='suvarchal.kumar@gmail.com',
    license="MIT",
    description="IDV scripts to teleport bundles",
    #long_description=read('README.md'),
    scripts=['bin/idv_teleport'],
    classifiers=[
    'Development Status :: 4 - Beta',

    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
]
)

