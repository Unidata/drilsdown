Use cases
=========
A few definitions:

ramadda_server
              refers to the RAMADDA_ server root directory; usually it is the whole path that ends with ``/repository``. For example ``https://weather.rsmas.miami.edu/repository``.  

entryid 
        refers to a RAMADDA_ entryid of a directory where user would like to publish the files and has access. For instance in url ``https://weather.rsmas.miami.edu/repository/entry/show?entryid=30c863d8-e68c-4722-8d4a-e2d25d79a710`` entryid would be ``30c863d8-e68c-4722-8d4a-e2d25d79a710``.

username
         refers to username of the user for the RAMADDA_ server.
password
         refers to password of user **username** for the RAMADDA_ server.


Publishing a file
~~~~~~~~~~~~~~~~~
ramadda_publish_ infers the file type automatically using the file extension.
To publish a file named ``testfile.ipynb`` use::

  ramadda_publish testfile.ipynb entryid -ramadda ramadda_server -user username -password password 

Publishing a file with an attachment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
RAMADDA_ files can have accompanying attachments. Image type attachments will be displayed as thumbnails for the file. 
To publish a file named ``testfile.xidv`` with an atachment ``attachmentfile.gif`` use::

  ramadda_publish testfile.xidv entryid -a attachmentfile.gif -ramadda ramadda_server -user username -password password


Publishing multiple files
~~~~~~~~~~~~~~~~~~~~~~~~~
To publish files with pattern `*.zidv` use::
  
   ramadda_publish '*.zidv' entryid -ramadda ramadda_server -user username -password password 

note the quotes around ``'*.zidv'`` in the command above. quotes are needed when file patterns are used.

Publishing multiple files with multiple attachments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To publish files with pattern `abc*.zidv` and a corresponding attachment `abc*.gif` use::

   ramadda_publish 'abc*.zidv' entryid -a 'abc*.gif' -ramadda ramadda_server -user username -password password 

Make sure the number of files and attachments are same, otherwise ramadda_publish_ publishes just the files to avoid any mismatch.

Publising a directory
~~~~~~~~~~~~~~~~~~~~~
To publish a directory named ``test_dir`` containing multiple files inside to RAMADDA_ use::
   
    ramadda_publish test_dir entryid -ramadda ramadda_server -user username -password password

Directories can be grouped as a RAMADDA_ casestudy with an additional keyword suffix ``-groupas casestudy``; this type of directory gets a special look when it contains jupyter notebooks within. For example this url ``https://weather.rsmas.miami.edu/repository/entry/show?entryid=f34a263b-afe6-46fa-9490-42e9689b38a6`` is a casestudy type.
 


.. _RAMADDA: https://www.geodeystems.com 
.. _ramadda_publish: ./index.html
