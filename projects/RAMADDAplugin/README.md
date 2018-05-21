
This is the package for the drilsdown RAMADDA plugin

The [ramaddaplugin.jar](https://github.com/Unidata/drilsdown/blob/master/plugins/ramaddaplugin.jar) is the publisher plugin for the IDV

The [drilsdownplugin.jar](https://github.com/Unidata/drilsdown/blob/master/plugins/drilsdownplugin.jar) is the plugin for RAMADDA that provides some drilsdown specific functionality


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

