import os
import pip
from six import iteritems
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install

PACKAGE_NAME = 'drilsdown'
SOURCES = {
    'jython-kernal': 'projects/IJython',
    'ipython-IDV': 'projects/ipython-IDV',
}


def install_drilsdown_projects(sources, develop=False):
    """ Use pip to install all drilsdown projects.  """
    print("installing all drilsdown projects in {} mode".format(
              "development" if develop else "normal"))
    wd = os.getcwd()
    for k, v in iteritems(sources):
        try:
            os.chdir(os.path.join(wd, v.root_dir))
            if develop:
                pip.main(['install', '-e', '.'])
            else:
                pip.main(['install', '.'])
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
    version="2.4.1",
    author="Drilsdown team",
    author_email="drilsdown@unidata.ucar.edu",
    description="A collection of tools for jupyter notebooks",
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
        'ipython-IDV',
        'jython-kernel',
    ],
    cmdclass={
        'install': InstallCmd,
        'develop': DevelopCmd,
    },

)