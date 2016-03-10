# colmet_web
Colmet visualization web tool

A web interface to colmet data extraction and graphs.
The most working project is currently into :
  
  ``protos/flask_mpld3_oarapi``
  
It's written in Python, uses Flask as the framework, Mpld3 for graph generation and 
the OAR API (>= 2.5.6) to extract the colmet data.

Installation:
-------------

- Check API_COLMET_EXTRACT_PATH and API_COLMET_HDF5_PATH_PREFIX variables into oar.conf
- Install python packages dependencies:
  - numpy
  - h5py
  - matplotlib
  - mpld3
  - flask
- Configure the variables at the top of ``protos/flask_mpld3_oarapi/colmet_web.py`` (SCRIPT_NAME is for
  setting the base URI of the installed framework, useful if you set up a reverse-proxy)

Launching:
---------
```
   cd protos/flask_mpld3_oarapi
   python ./colmet_web.py
```

Point your browser to ``http://localhost:5000``
