[![Build Status](https://travis-ci.org/Unidata/ipython-IDV.svg?branch=master)](https://travis-ci.org/piqueen314/ipython-IDV)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
# ipython-IDV
### Part of the [EarthCube DRILSDOWN project](https://brianmapes.github.io/EarthCube-DRILSDOWN/)

Extension for IPython Notebooks to provide line and cell magics to call out to Unidata's [Integrated Data Viewer](https://github.com/Unidata/IDV) 

### To set it up:

1. After installing Jupyter/iPython notebook software [like this](https://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/), you will also need to install the [ipywidgets package](https://ipywidgets.readthedocs.io/en/latest/user_install.html)

2. Once Jupyter/iPython is ready, copy [drilsdown.py](https://github.com/Unidata/ipython-IDV/blob/master/drilsdown.py) to your local extensions directory, _~/.ipython/extensions_

3. To run IDV commands from the Notebook, you will need to have installed [IDV version 5.4 or later](http://www.unidata.ucar.edu/software/idv/nightly/). Also, you need to set your IDV_HOME environment variable to be the IDV install directory, so that python can execute the command ${IDV_HOME}/runIDV

4. You also need to configure your IDV to accept connections from the ipython notebook. To do this set the following property in your local ~/.unidata/idv/DefaultIdv/idv.properties file:

<pre>
idv.monitorport = 8765
</pre>


--------
### Now you've done the 4 steps above. 
When you launch _jupyter notebook_, and run an iPython notebook in your browser, do this in the notebook:

<pre>
%load_ext drilsdown
</pre>

That will give you a dashboard-style view of many of the ways the Notebook can launch and interact with The IDV, and find resources such as existing bundles, data catalogs, and more, including a link to the help section.


If you plan on writing Python code in this notbeook (rather then merely capturing images and notes about a case study IDV session), you should import the Idv and Ramadda classes:

<pre>
from drilsdown import Idv
from drilsdown import Ramadda
</pre>

We welcome your use cases! Email mapes at miami dot edu. See examples [below](https://github.com/Unidata/ipython-IDV/blob/master/README.md#examples).

---------
#### Publishing to RAMADDA, using the IDV's capabilities

If you want to enable your IDV to publish to a RAMADDA server, get [ramaddaplugin.jar](https://github.com/Unidata/ipython-IDV/blob/master/ramaddaplugin.jar). Copy this file to your local IDV plugins directory (~/.unidata/idv/DefaultIdv/plugins). While it is not a plain text code file, it is included in this repo so all of the products that are required for running drilsdown can be found in 
one place.

---------
#### Setting up your own RAMADDA to handle DRILSDOWN Case Study objects

If you operate a RAMADDA, and want it to host DRILSDOWN _Case Study_ digital objects, get [drilsdownplugin.jar](https://github.com/Unidata/ipython-IDV/blob/master/drilsdownplugin.jar), put it in your RAMADDA installation's _plugins_ area, and restart. It is produced from the code at [RAMADDA drilsdown repository](https://github.com/Unidata/drilsdown) but is included here so all of the products that are required for running drilsdown can be found in one place.



<h2>Examples of Python notebooks calling DRILSDOWN and The IDV:</h2>
Here is an example of how to use the API to load an IDV bundle with different bounding boxes and capture images

<pre>
from drilsdown import Idv
Idv.fileUrl="http://geodesystems.com/repository/entry/get?entryid=d83e0924-008d-4025-9517-394e9f13712f"
bboxes = [[50,-130,40,-100],[50,-100,40,-75],[40,-130,20,-100],[40,-100,20,-75]]
for i in range(len(bboxes)):
    bbox=bboxes[i];
    Idv.loadBundle(Idv.fileUrl,bbox)
    Idv.makeImage(caption="BBOX:" + repr(bbox[0]) +"/" + repr(bbox[1]) +"  " + repr(bbox[2]) +"/" + repr(bbox[3]))
</pre>


<pre>
from drilsdown import Idv
Idv.fileUrl="http://geodesystems.com/repository/entry/get?entryid=d83e0924-008d-4025-9517-394e9f13712f"
bboxes = [[50,-130,40,-100],[50,-100,40,-75],[40,-130,20,-100],[40,-100,20,-75]]
for i in range(len(bboxes)):
    bbox=bboxes[i];
    Idv.loadBundle(Idv.fileUrl,bbox);
    label = "BBOX:" + repr(bbox[0]) +"/" + repr(bbox[1]) +"  " + repr(bbox[2]) +"/" + repr(bbox[3]);
    Idv.makeMovie(caption=label,display=True, publish={'parent':'9adf32b5-aad4-4a8d-997e-216b9757d240',"name":"Image #" + repr(i)})
</pre>




The makeImage can take one of 2 forms of a publish argument. The first is a boolean and will result in the IDV popping up its RAMADDA publish dialog box where the image can be published.
<pre>
    Idv.makeImage(caption=label, publish=True);
</pre>

In the second form the publish argument is a map. This directs the python to do the publishing directly to RAMADDA. The map can contain a parent member which is the entry id to publish to and a name member which is the entry name. 

<pre>
    Idv.makeImage(caption=label, publish={'parent':'9adf32b5-aad4-4a8d-997e-216b9757d240',"name":"Image #" + repr(i)})
</pre>

To enable direct publishing to RAMADDA you need to have your RAMADDA user name and password defined as environment variables:

<pre>
export RAMADDA_USER=
export RAMADDA_PASSWORD=
</pre>


