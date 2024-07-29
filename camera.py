import time
import datetime
import requests
import os

from picamera2 import Picamera2,Preview
from picamera2.encoders import H264Encoder
from gpiozero import MotionSensor
from signal import pause

# Initialize the camera and motion sensor
camera = Picamera2()
camera_config = camera.create_still_configuration(main={"size":(1920,1080)},lores={"size":(640,480)},display="lores")
camera.configure(camera_config)
video_config = camera.create_video_configuration()
camera.configure(video_config)
pir = MotionSensor(4)

def send_notification():
    requests.post('https://api.mynotifier.app',{"apiKey":os.environ['MYNOTIFIER_API_KEY'],"message": "test","description":"test message","type":"info"})

datetime.datetime.now()
print (datetime.datetime.now(),': Starting Monitor...')

def capture_snapshot_and_video():

    camera.start()
    #send_notification()

    # Capture a snapshot
    snapshot_filename = '/opt/trail_cam/capture/'+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.jpg'
    camera.capture_file(snapshot_filename)
    print(f"Snapshot saved as {snapshot_filename}")
    
    # Start recording video
    encoder = H264Encoder(10000000)
    video_filename = '/opt/trail_cam/capture/'+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.h264'
    camera.start_recording(encoder,video_filename)
    print(f"Recording started: {video_filename}")
    
    # Record for 30 seconds
    time.sleep(30)
    
    # Stop recording
    camera.stop_recording()
    print(f"Recording stopped: {video_filename}")

# Set up the motion sensor to call the function when motion is detected
pir.when_motion = capture_snapshot_and_video

# Keep the script running
pause()
