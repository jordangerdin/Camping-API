# Camping-API

This application combines multiple APIs:
* OpenCage Geocoder
* HikingProject
* Mapbox
* OpenWeatherMap

These API's allow a user to get all sorts of information about hiking trails anywhere in the world.
You can search a location and receive a list of nearby trails, and can select specific trails to get a map of the area or the current 5 day forecast.
You can also save a location and bookmark it for later, and view all the trails you have bookmarked. 

# TO RUN:

After getting everything from requirements.txt, in your terminal type "set FLASK_APP=main.py" (windows) or export "FLASK_APP=routes.py"(mac/linux)
then type "flask run". It should say a server is running on http://127.0.0.1:5000. Go to that URL and you should be able to use the app.
