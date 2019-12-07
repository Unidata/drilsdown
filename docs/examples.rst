==============================
Examples of DRILSDOWN projects
==============================

Basic Examples
--------------

.. toctree::
   :maxdepth: 1
   :glob:
 
   examples/Basic_Examples/*


Atmospheric (observed): What do clouds look like where they are acting to increase the water vapor?
---------------------------------------------------------------------------------------------------
One example of "drilling down" is to view satellite imagery around places where interesting quantitative meteorology is diagnosed. (This example)[https://github.com/Unidata/drilsdown/tree/master/UseCase_Examples/WaterVaporTendencies] constructs URLs  to a NASA imagery server, from the date and time information around extreme values of a *Lagrangian water vapor tendency*.

The next level of scientific inquiry here is to call up a vertical sounding display, from a global 3D meteorological analysis, in either the IDV or a Jupyter Python session.

These headers within the .ipynb notebook may help clarify the workflow:

.. toctree::
   :maxdepth: 2
   :glob:

   examples/WaterVaporTendencies/MIMIC_AT_2deg_URLs_clickmap.ipynb

Atmospheric (observed): How do watervapor "islands" last long over the dry western-equatorial Indian Ocean?
-----------------------------------------------------------------------------------------------------------
Over the western equatorial Indian ocean, which is usually dry, there are occasional periods when filaments or "islands" of water vapor in the atmopshere are brought by the winds.
These last surprisingly long, even as rain acts to remove the vapor. We wanted to study several such instances using vertical profile probes and column water vapor maps over region bounded by 17, 36 ; -15, 90 (North , West ; South, East).

A `list
<https://github.com/unidata/drilsdown/blob/master/UseCase_Examples/INDIANOCEAN_WATERVAPOR_ISLANDS/Igel_WEIO_case_list.txt>`_ of begin and end dates was supplied by by Dr. Matt Igel of UC-Davis, based on his blob-tracking results applied to column water vapor (CWV).

A script is generated to teleport the simple IDV `bundle <https://weather.rsmas.miami.edu/repository/entry/get?entryid=84d7e564-fcf2-48c9-82fb-bae358622333>`_ to a zidv bundle comprising of 3D data from two reanalysis for the lat-lon bounding box 17 - 36 , -15 - 90 (North - West ,South - East).

.. toctree::
   :maxdepth: 2
   :glob:

   examples/INDIANOCEAN_WATERVAPOR_ISLANDS/generate_teleport_script.ipynb

Generated teleport bash `script <https://github.com/unidata/drilsdown/blob/master/UseCase_Examples/INDIANOCEAN_WATERVAPOR_ISLANDS/teleport_Igel_WEIO_cases.sh>`_ was run in a headless linux environment to generate zidv files.
These zidv case `files <https://weather.rsmas.miami.edu/repository/entry/show?entryid=a4154517-ac1c-4eb4-b842-572cb55ce1f2>`_ are then published to RAMADDA server using following command::

  ramadda_publish 'Igel_WEIO*.zidv' a4154517-ac1c-4eb4-b842-572cb55ce1f2 -a 'Igel_WEIO*.gif' -username user -password pass


Links for these command line utilities: `IDV_teleport <https://unidata.github.io/drilsdown/IDV_teleport.html>`_ , `RAMADDA_publish <https://unidata.github.io/drilsdown/RAMADDA_publish.html>`_

Atmospheric (complex, simulated): What is going on in areas where small scales are adding energy to the large-scale flow?
-------------------------------------------------------------------------------------------------------------------------
In this project, a global model with 7km mesh produced an enormous dataset including vertical flux of horizontal momentum (u'w' and v'w'). The notebooks below show some "drilling down" results.

These headers within two of the .ipynb notebooks in examples/MomentumFlux_in_GlobalCloudmodel show the workflow:

.. toctree::
   :maxdepth: 2
   :glob:

   examples/MomentumFlux_in_GlobalCloudmodel/notebooks_as_of_2017-July10/SKEdot_climatology_and_timeseries.ipynb
   examples/MomentumFlux_in_GlobalCloudmodel/notebooks_as_of_2017-July10/Planview_eddyflux_SKEdot_interactiveplots.ipynb
   examples/MomentumFlux_in_GlobalCloudmodel/notebooks_as_of_2017-July10/Profile_eddyflux_SKEdot_interactiveplots.ipynb   
   examples/MomentumFlux_in_GlobalCloudmodel/notebooks_as_of_2017-July10/Cumulus_friction_coefficient.ipynb               

Atmospheric: Weather events case studies.
-----------------------------------------
.. toctree::
   :maxdepth: 2
   :glob:
   
   examples/Weather_Event_Case_Study/*

Oceanic: What's going on when the Loop Current in the Gulf of Mexico splits off an eddy?
----------------------------------------------------------------------------------------

.. toctree::
   :maxdepth: 2
   :glob:
    
   examples/Ocean_Loop_Current/*

