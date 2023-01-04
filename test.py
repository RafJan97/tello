import time, cv2
from threading import Thread
from djitellopy import Tello

tello = Tello()

tello.connect()

keepRecording = True
tello.streamon()
frame_read = tello.get_frame_read()

# time.sleep(10)

def videoRecorder():

    # while keepRecording:
        cv2.imshow('Tello Camera', frame_read.frame)
        time.sleep(1 / 30)


recorder = Thread(target=videoRecorder)
recorder.start()

time.sleep(60)
# cv2.waitKey()
# cv2.destroyAllWindows()