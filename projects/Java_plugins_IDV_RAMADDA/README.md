
## DRILSDOWN project plugins for Java applications (IDV and RAMADDA)

The [ramaddaplugin_forIDV.jar](https://github.com/Unidata/drilsdown/blob/master/projects/Java_plugins_IDV_RAMADDA/plugins/ramaddaplugin_forIDV.jar) is a plugin for the IDV. It is now available directly through the [IDV's Plugins menus as explained here](https://www.unidata.ucar.edu/software/idv/docs/userguide/misc/Plugins.html).

The [drilsdownplugin_forRAMADDA.jar](https://github.com/Unidata/drilsdown/blob/master/projects/Java_plugins_IDV_RAMADDA/plugins/drilsdownplugin_forRAMADDA.jar) is a plugin for RAMADDA that provides some drilsdown specific functionality (such as rendering of Case Study entry types).

--------------------
### ... the below may include out of date folder names on this repo...
To build from source:
This plugin relies on the RAMADDA source tree available at Github https://github.com/geodesystems/ramadda
Install the RAMADDA tree as a sibling of the drilsdown dir
e.g. - 

<pre>
source
  |
  +------ drilsdown
  |          |
  |          + projects/RAMDDAplugin/ramadda
  |          
  |
  +------ ramadda (from Github)
</pre>



To build run:
cd ramadda
ant

This runs the ant script in src/edu/miami/drilsdown

The plugin will be placed in the ramadda/dist directory

---------

In order to have .ipynb files rendered on RAMADDA by jupyter's nbconvert service, you have to install jupyter and add this line to .properties file in your ramadda home directory, or to repository.properties in a Tomcat installation: 

*ramadda.jupyter.path=/path/to/jupyter*

