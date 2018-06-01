==================
Installation Guide
==================

------------
Requirements
------------

------------
Installation
------------
Tier I: IDV enhancements only
  Install the latest (nightly build) of IDV `here <https://www.unidata.ucar.edu/downloads/idv/nightly/index.jsp>`_. 

Tier II: IDV interactions with jupyter + iPython
  In addition to the IDV, install jupyter, for instance using `Anaconda <http://jupyter.org/install>`_. 

Tier III: Storing and servicing {IDV, Jupyter} "Case Studies" on RAMADDA
  In addition to the IDV and Jupyter, you need 
    1. Access (username and password, or knowledge of an anonymous-accessible area) granted by the Admin of a RAMADDA repository. 
    2. In order to publish your {IDV, Jupyter} "Case Studies" you should install the `RAMADDA plugin to IDV <https://github.com/Unidata/drilsdown/tree/master/projects/RAMADDAplugin>`_.

Tier IV: RAMADDA installation with DRILSDOWN functionality
  To install your own RAMADDA repository, follow instructions `here <https://geodesystems.com/?>`_ 
  Then, put `drilsdownplugin.jar <https://github.com/Unidata/drilsdown/blob/master/projects/RAMADDAplugin/plugins/drilsdownplugin.jar>`_  in your repository's plugins/ directory, and restart it. 
  
  To have your Case Study .ipynb files rendered by jupyter's nbconvert service, install jupyter on your RAMADDA's host machine, and add this line to .properties file in your ramadda home directory (or to repository.properties, in a Tomcat installation):
  
    *ramadda.jupyter.path=/path/to/jupyter* 

--------
Examples
--------
Use case examples, with template .xidv IDV bundles and .ipynb Jupyter notebooks, are at: 

  **Observed atmopsheric states in areas where column integrated water vapor is increasing quickly.** 
  
  

