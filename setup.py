import os
from six import iteritems
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
import subprocess

PACKAGE_NAME = 'drilsdown'
SOURCES = {
   'ipython_IDV': 'projects/ipython_IDV',
   'idv_teleport': 'projects/IDV_teleport',
   'ramadda_publish': 'projects/RAMADDA_publish',
}
VERSION = '2.4.91'

def install_drilsdown_projects(sources, develop=False):
    """ Use pip to install all drilsdown projects.  """
    print("installing all drilsdown projects in {} mode".format(
              "development" if develop else "normal"))
    wd = os.getcwd()
    for k, v in iteritems(sources):
        try:
            os.chdir(os.path.join(wd, v))
            if develop:
                subprocess.check_call(['pip', 'install', '-e', '.']) # could be pip3 on certain platforms
            else:
                subprocess.check_call(['pip', 'install', '.']) # could be pip3 on certain platforms
        except Exception as e:
            print("Oops, something went wrong installing", k)
            print(e)
        finally:
            os.chdir(wd)


class DevelopCmd(develop):
    """ Add custom steps for the develop command """
    def run(self):
        install_drilsdown_projects(SOURCES, develop=True)
        develop.run(self)


class InstallCmd(install):
    """ Add custom steps for the install command """
    def run(self):
        install_drilsdown_projects(SOURCES, develop=False)
        install.run(self)


setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author="Drilsdown team",
    author_email="drilsdown@unidata.ucar.edu",
    description="A collection of tools for jupyter notebooks",
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    url="https://github.com/Unidata/drilsdown",
    license="MIT",
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'future',
        'six',
        'requests',
        'ipython',
        'ipywidgets>=7.1.0rc',
        'jupyter-client',
#        'ipython_IDV>=' + VERSION + "'", # cannot be source and a dependency??
        'ipython-IDV', # from pypi
        'ramadda_publish', #from pypi
        'idv_teleport', #from pypi
    ],
    cmdclass={
        #'install': InstallCmd, # do not overwrite for now to make 
                                # pip install and python setup.py install do same.
                                # note in class pip might be called pip3 on certain platforms
        'develop': DevelopCmd,
    },
    extras_require={
        'addons': ['numpy','netcdf4','xarray','metpy'],
        'visual': ['pyviz'],
    }
)
