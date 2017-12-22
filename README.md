
This is the package for the drilsdown RAMADDA plugin

The [ramaddaplugin.jar](https://github.com/Unidata/drilsdown/blob/master/plugins/ramaddaplugin.jar) is the publisher plugin for the IDV

The [drilsdownplugin.jar](https://github.com/Unidata/drilsdown/blob/master/plugins/drilsdownplugin.jar) is the plugin for RAMADDA that provides some drilsdown specific functionality


To build from source:
This plugin relies on the RAMADDA SVN tree to be installed as a sibling of this  directory. 
e.g. - 

<pre>
source
  |
  +------ drilsdown
  |          |
  |          +-----ramadda
  |                  |
  |                  +---- src ...
  |          
  |
  +------ ramadda-code
</pre>

Get the RAMADDA source with:
svn checkout svn://svn.code.sf.net/p/ramadda/code/ ramadda-code


To build run:
cd ramadda
ant

This runs the ant script in src/edu/miami/drilsdown

The plugin will be placed in the ramadda/dist directory