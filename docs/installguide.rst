==================
Installation Guide
==================

------------
Requirements
------------
The IDV (unidata.ucar.edu/idv) is an all-platform, click-to install visualization package.



The IDV is oriented toward GUI operation on single-user workstations with screens,
but sysadmins can install it on multiuser servers, and it can run headless
(without the GUI or screen) for scripted services using the IDV Scripting Language (ISL, suffix .isl).
In fact, .isl scripting underlies many DRILSDOWN capabilities.

------------
Installation
------------
Tier I: IDV and our enhancements

  Install the latest version of IDV `here <https://www.unidata.ucar.edu/downloads/idv/nightly/index.jsp>`_.
  The newest DRILSDOWN developments go into the *nightly build* (currently, version 5.5u1), so
  this link directs you to that.

  Within the IDV, perform menu operations under Tools-->Plugin Manager to install
  Customized IDVs --> MapesIDVcollection.jar (the .jar is stored in this repo).

  Install a command-line tool called ``idv_teleport``. This is a user-friendly translator to .isl scripts
  that will replace or 'teleport' the displayed area and time range of
  an existing ('template') code-only IDV bundle (.xidv file).
  If template.xidv uses data sources that are large aggregations (local or remote), then
  idv_teleport can turn a list of space-time coordinates ('case coordinates') into a set of
  zipped IDV code+data (.zidv) files containing identical, arbitrarily complex 3D displays
  of basic and derived quantities for those cases, in a background or batch mode.

Tier II: IDV interactions with jupyter + iPython
  In addition to Tier I, install jupyter, for instance using `Anaconda <http://jupyter.org/install>`_.

  Install our iPython extension, drilsdown.py, from pip or conda.
      ``pip install drilsdown`` or ``conda install drilsdown``

Tier III: Storing and servicing {IDV + Jupyter} "Case Studies" on RAMADDA
  In addition to the IDV and Jupyter, you need
    1. Access (username and password, or knowledge of an anonymous-accessible area) granted by the Admin of a RAMADDA repository.
    2. In order to publish your {IDV + Jupyter} "Case Studies" you should install the `RAMADDA plugin to IDV <https://github.com/Unidata/drilsdown/tree/master/projects/RAMADDAplugin>`_. This is available in the IDV's Tools-->Plugin manager. 
        
Tier IV: Install your own RAMADDA with DRILSDOWN functionality
  To install a RAMADDA repository, follow instructions `here <https://geodesystems.com/?>`_
  Then, put `drilsdownplugin.jar <https://github.com/Unidata/drilsdown/blob/master/projects/RAMADDAplugin/plugins/drilsdownplugin.jar>`_  in your repository's plugins/ directory, and restart it.

  To have your Case Study .ipynb files rendered by jupyter's nbconvert service, install jupyter on your RAMADDA's host machine, and add this line to .properties file in your ramadda home directory (or to repository.properties, in a Tomcat installation):

    *ramadda.jupyter.path=*``/path/to/jupyter``

--------
Examples
--------
Use case examples, with template .xidv IDV bundles and .ipynb Jupyter notebooks, are at:

  **Observed atmospheric states in areas where column integrated water vapor is increasing quickly.**
