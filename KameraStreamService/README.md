# README for KameraStreamService

This folder can be used to stream the input of a camera to a website created by it the device it is connected to. 

Prerequisites:  1. OpenCv python https://pypi.org/project/opencv-python/
                2. pypylon and hence pylon  https://github.com/basler/pypylon
                3. flask https://flask.palletsprojects.com/en/2.0.x
                
To run the application, navigate into the BaslerStreamSite folder, execute "export FLASK_APP=webstreaming" followed by execution of "flask run --host={IP of the device}"
The website will be visible under "http://{IP of the device}:5000/
  
For the RPi which is installed in the Rahm-lab: the export command should automatically be executed at the creation of a new shell.
