Installation
=================

The easiest way to install IDV_teleport_ is:

     ``pip install idv_teleport``

To update an existing installation use:
 
     ``pip install --upgrade idv_teleport``

IDV_teleport_ is currently untested in Windows based operating systems.

Requirements
~~~~~~~~~~~~~
IDV_ software is needed. To let the utility know the installation of IDV_ in the current environment, environment variable 
IDV_HOME needs to be set to IDV_ installation directory. 

For instance in 

BASH environment:

     `export IDV_HOME=/path/to/IDV_5.4u1`

CSH environment:

     `setenv IDV_HOME /path/to/IDV_5.4u1`

for MacOS users the path is typically in `/Applications/IDV_5.4u1`
      
IDV_teleport_ can run in headless mode. To enable headless mode a virtual X server utility Xvfb_ is needed.

.. _Xvfb: https://www.x.org/releases/X11R7.6/doc/man/man1/Xvfb.1.xhtml
.. _IDV: https://www.unidata.ucar.edu/software/idv
.. _Bundle: https://www.unidata.ucar.edu/software/idv/docs/userguide/Bundles.html


.. _IDV_teleport: https://suvarchal.github.io/IDV_teleport
