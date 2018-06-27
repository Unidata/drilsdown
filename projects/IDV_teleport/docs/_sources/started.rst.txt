Getting Started
================
Installation_ can be checked using by executing the command::

    idv_teleport -h

The above command shows list of options that can be used.


As as example download this fairly complex sample bundle `HYCOM_3dvort_template.xidv <http://earthcube.ccs.miami.edu:8080/repository/entry/get?entryid=0dcfbd52-76b5-44aa-85cf-7d79efad7b62>`_. 

Shell
~~~~~~~~~~~~~~~~
Check setting up of the IDV path by opening the bundle::

    $IDV_HOME/runIDV HYCOM_3dvort_template.xidv

Now to teleport the bundle to time `1992-10-14` and `+- 2days` around bounding box (North West South East)  `30 -90 20 -82`::
    
    idv_teleport -b HYCOM_3dvort_template.xidv -t 1992-10-14 -td 2days -bbox 30 -90 20 -82 

This should create 3 files in the same directory named::

    HYCOM_3dvort_template_1992-10-14-00-00-00.gif  
    HYCOM_3dvort_template_1992-10-14-00-00-00.zidv
    HYCOM_3dvort_template_1992-10-14-00-00-00.png  

The ``.zidv`` file contains data included visulization bundle that can be opened by IDV. ``.gif`` is the animation of visualization produced. 

To run in headless mode (if the tool ``Xvfb`` is present) append the above shell command by ``-nohead True``.

Bundles produced using the tool are in Demos_ Section.

Jupyter Notebook/Python
~~~~~~~~~~~~~~~~~~~~~~~
NOTE: Currently the API to import IDV_teleport_ from python is under development and is expected to be released in the next version. Below code snippet gives tentative API.::

    from idv_teleport import teleport
    teleport('bundlefile.xidv','2010-01-01','2days','30 -90 20 -82',headless=True)

API leads to convinient scripting from python like::

    for dates in ['2010-01-01','2008-07-01']:
         teleport('bundlefile.xidv','2010-01-01','2days','30 -90 20 -82',headless=True)

.. _IDV_teleport:
.. _Installation: 
.. _requirements: 
.. _Demos:

