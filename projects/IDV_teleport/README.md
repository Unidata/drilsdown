[![Build Status](https://travis-ci.com/suvarchal/IDV_teleport.svg?branch=master)](https://travis-ci.com/suvarchal/IDV_teleport)
# IDV_teleport
Script to relocate the space-time bounding box of one or more existing (‘template’) IDV bundles and then execute runIDV to fetch the data and write ouputs.

Outputs (3): Thumbnail image; Animation; and Zipped .zidv file containing all data and displays. All are called CASE_NAME.xxx with appropriate xxx suffixes. 

Arguments are used to specify -bbox in lat-lon space, and one or a list of temporal ranges. Time ranges are specified as a middle time of the desired time sequence (-t) plus a half-width of the sequence (-td). The temporal stride must be set in the template BUNDLE.xidv, and can only be changed in the IDV GUI.

Requirements: Version 5.3u1 from May 2016 or later [IDV](http://www.unidata.ucar.edu/software/idv/nightly/), and any Python. 

Usage:

       idv_teleport.py [-h] -t TIME -b BUNDLE [BUNDLE ...] [-td TIMEDELTA]
                       [-bbox NORTH WEST SOUTH EAST]
                       [-case CASE_NAME [CASE_NAME ...]]
                       [-outdir OUTPUT_DIRECTORY] [-d {True,False}]
                       [-purl PUBLISH_URL]
      
      
Optional arguments:

	-h, --help               show this help message and exit
    -b BUNDLE.xidv [BUNDLE2.xidv ...], --bundle BUNDLE.xidv [BUNDLE2.xidv ...]
                             IDV Bundle template file (local file or remote URL).
				 Can also be .zidv file.
	-bbox NORTH WEST SOUTH EAST, --boundingbox NORTH WEST SOUTH EAST
                             Set the bounding box of the bundle with boundaries
                             north, west, south, east
	-t TIME, --time TIME  Input central time as YYYY-MM-DD (optionally with hh:mm:ss),
                             or as a text file with times as above, one per line.						 
	-td TIMEDELTA, --timedelta TIMEDELTA
                             Time delta as Nseconds, Nhours, Ndays, Nweeks…
                             Output bundle will be centered (TIME +- TIMEDELTA).
                             Default is 0seconds. 
	-case CASE_NAME [CASE_NAME2 ...], --case_name CASE_NAME [CASE_NAME ...]
                             Case name to prefix the bundle; by default, the case name
                             will be selected from template bundle file
	-outdir OUTPUT_DIRECTORY, --output_directory OUTPUT_DIRECTORY
                             Set the output path to place the output;default is
                             current directory from where the script is run
	-pubid PUBLISH_ID, --publish_id PUBLISH_ID
                        Publish bundle and image at a RAMADDA server;argument
                        shoud be ramadda entryid wherethe user from
                        environment variable RAMADDA_USER and password from
                        RAMADDA_PASSWORD has permissionsto write files.
	-nohead {True,False}, --headless {True,False}
                        Option to use headless display environment or not to
                        use headless environment `Xvfb` needs to be
                        installed and be present in the PATH. Default is set to True for convinience,
			    When True and Xvfb is not on path it tries to run IDV with default local display.
	-d {True,False}, --debug {True,False}
                        Debug option; for each time in timefile, IDV session
                        will remain open and MUST be closed manually


Simplest use case: 

     python idv_teleport.py -b templatebundlefile.xidv -t YYYY-MM-DD_hh:mm:ss
