# RAMADDA_publish
Allows automated ways of publishing content to a RAMADDA server.
https://suvarchal.github.io/RAMADDA_publish/

    Usage: 

       ramadda_publish [-h] [-groupas {plain,casestudy}] [-a ATTACHMENT]
                       [-ramadda RAMADDA] [-user USER] [-password PASSWORD]
                       publish_file entryid


       positional arguments:

       publish_file          Publish a file or directory or multiple files (with a
                             unix pattern) to a RAMADDA server;Currently supports
                             publishing IDV bundles, Jupyter notebooks, gridded
                             data files(netcdf,grib...), csv files, other formats
                             are published as plain files
                        
       entryid               Parent entryid string on a RAMADDA server.It should
                             contain just the string NOT entire url path.NOTE:
                             RAMADDA_USER needs to have permissions for publishing
                             the file on the RAMADDA server

       optional arguments:
       -h, --help            show this help message and exit
       -groupas {plain,casestudy}
                             when the published file is a directory, it can be
                             either a plain directory or a casestudy type of
                             directory. (default: plain)
       -a ATTACHMENT, --attachment ATTACHMENT
                             Publish this file or file pattern as an
                             attachment.NOTE: Number of files and attachments
                             should be the same.Currently only image files are
                             supported (default: None)
       -ramadda RAMADDA, --ramadda RAMADDA
                             The RAMADDA server.By default RAMADDA environment
                             variable is used, if it is absent the url
                             https://weather.rsmas.miami.edu/repositoryis used.
                             (default: None)
       -user USER, --user USER
                             User for RAMADDA, by default, if exists, the
                             environment variable RAMADDA_USER is used as a user.
                             (default: None)
       -password PASSWORD, --password PASSWORD
                             Password for -user or RAMADDA_USER, by default, if
                             exists, the environment variable RAMADDA_PASSWORD is
                             used as a user password. (default: None)

    Some examples: 
    To publish a file at an entryid of a ramadda server
        ramadda_publish file_to_publish publish_at_entryid

    To publish files with pattern say '*.zidv'  at an entryid of a ramadda server
        ramadda_publish '*.zidc' publish_at_entryid
    note the quotes while using a pattern

    To publish a file at an entryid of a ramadda server with an attachment
        ramadda_publish file_to_publish publish_at_entryid -a attachment_file

    To publish a files with a pattern say '*.zidv' with corresponding attachment pattern '*.gif'  
    at an entryid of a ramadda server
        ramadda_publish '*.zidv' publish_at_entryid -a '*.gif'
    note the number of files for pattern should be same for attachments

    To publish a directory at an entryid of a ramadda server as a simple directory with all files within.
        ramadda_publish directory_to_publish publish_at_entryid  

    To publish a directory at an entryid of a ramadda server as a case study directory with all files within.
        ramadda_publish directory_to_publish publish_at_entryid -groupas casestudy`
