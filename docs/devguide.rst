====================
Infrastructure Guide
====================

----------
Versioning
----------

---------
Releasing
---------

-------------
Documentation
-------------

Live notebooks capability (Suvarchal May 2019): I used traefik for reverse proxy, a flask app implementing simple API for spawning docker containers of Jupyter notebooks.  API can be customized in flask further like: allocate more resources to a ramadda user, have custom environments for different drilsdown cases etc. src is hosted at https://github.com/suvarchal/nbapp for the interested, and docker compose file I used on the sandbox server is https://github.com/suvarchal/nbapp/blob/master/deploy/docker-compose.yml.   

