from codecs import open
from os import path

import setuptools

#from projects import __version__

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="ipython-IDV",
    version= '2.3.1',
    url="https://github.com/Unidata/ipython-IDV.git",
    author="Drilsdown team",
    author_email="drilsdown@unidata.ucar.edu",
    description="This project allows users to use Unidata's IDV with jupyter notebooks ",
    long_description=open('README.md').read(),
    packages = setuptools.find_packages(),
    py_modules = ['ipython-IDV'],
    install_requires=['ipython'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    # package_data={
    #     'ipython-IDV': [
    #         'drilsdownplugin.jar',
    #         'ramaddaplugin.jar',
    #
    #     ],
    # },
    # package_dir={"ipython-IDV": 'drilsdown_namespace'},
    # include_package_data=True,
)
