#!/usr/bin/python
# import the necessary packages

from flask import Response
from flask import Flask
from flask import render_template
from pypylon import pylon
import threading
import cv2
import os
os.environ["PYLON_CAMEMU"] = "1"

lock = threading.Lock()
# initialize a flask object
app = Flask(__name__)

# conecting to the first available camera
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

# Grabing Continusely (video) with minimal delay
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
converter = pylon.ImageFormatConverter()

# converting to opencv bgr format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned





@app.route("/")
def index():
    # return the rendered template
    return render_template("index.html", current_temperature=23)


def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock
    # loop over frames from the output stream
    while camera.IsGrabbing():
        with lock:
            grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            if grabResult.GrabSucceeded():
            
                 # Access the image data
                image = converter.Convert(grabResult)
            
                img = image.GetArray()
                # encode the frame in JPEG format
                (flag, encodedImage) = cv2.imencode(".jpg", img)
                #yield the output frame in the byte format
                if not flag:
                    continue
                yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
                bytearray(encodedImage) + b'\r\n')
                #time.sleep(0.002)
            grabResult.Release() 
            
        

@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
        mimetype = "multipart/x-mixed-replace; boundary=frame")



    


# check to see if this is the main thread of execution
if __name__ == '__main__':
   
    
    # start the flask app
    app.run(host="0.0.0.0", port=8000, debug=True,
        threaded=True, use_reloader=False)

