import cv2
from djitellopy import tello
from threading import Thread, Event
from simple_pid import PID
import keyboard
import calendar
import time
from csv import writer
import csv
import numpy as np
import math



# Current GMT time in a tuple format
current_GMT = time.gmtime()

# ts stores timestamp
ts = calendar.timegm(current_GMT)

file_name = "tello_data_" + str(ts) + ".csv"

# append_list_as_row(file_name,
#                    ["acc_x", "acc_y", "acc_z", "vel_x", "vel_y", "vel_z", "roll", "pitch", "yaw", "tof", "bat"])



class TelloController:
    class TelloKillSwitch(Thread):
        tc_handler = None

        def __init__(self, tc_handler):
            Thread.__init__(self)
            self.tc_handler = tc_handler

        def run(self):
            keyboard.wait('space')
            self.tc_handler.force_emergency_stop()

    class TelloTimer(Thread):
        interval = 1.0
        running = None
        func = None

        def __init__(self, interval, event, func):
            Thread.__init__(self)
            self.running = event
            self.interval = interval
            self.func = func

        def run(self):
            while not self.running.wait(self.interval):
                self.func()

    tello_drone = None
    stop_controller = None

    def force_emergency_stop(self):
        self.tello_drone.emergency()
        self.stop_controller.set()

    def getBatteryData(self):
        print("Battery status: ", self.tello_drone.get_battery())

    def saveData(self):

        file = open(file_name, 'a+', newline='')
        writer = csv.writer(file)
        data = [self.tello_drone.get_acceleration_x(), self.tello_drone.get_acceleration_y(),
                                 self.tello_drone.get_acceleration_z(),
                                 self.tello_drone.get_speed_x(), self.tello_drone.get_speed_y(),
                                 self.tello_drone.get_speed_z(),
                                 self.tello_drone.get_roll(), self.tello_drone.get_pitch(), self.tello_drone.get_yaw(),
                                 self.tello_drone.get_flight_time(), self.tello_drone.get_battery()]
        writer.writerow(data)
        file.flush()
        file.close()



    def checkBattery(self):
        if self.tello_drone.get_battery() < 20:
            print("Battery Low! ", self.tello_drone.get_battery())

    def takePicture(self):
        frame_read = self.tello_drone.get_frame_read()
        cv2.imwrite(str(ts) +".png", frame_read.frame)

    def showCameraStream(self):
        frame = np.zeros([720, 960, 3])

        frame[:] = (0.5, 0.5, 0.5)

        frame = self.frame_read.frame

        # blueImage = np.zeros([960, 720, 3])
        # blueImage[:] = (10, 10, 10)
        #
        # frame = blueImage

        # cv2.putText(frame, 'Tekst', (30, 200), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

        batt_val = self.tello_drone.get_battery()
        # batt_val = 55

        if (batt_val <= 34):
            colour = (0, 0, 255)
        elif (batt_val < 60):
            colour = (0, 127, 255)
        else:
            colour = (0, 255, 0)

        cv2.putText(frame, 'BATT: ' + str(batt_val) + "%", (20, 700), cv2.FONT_HERSHEY_COMPLEX, 1, colour, 2)

        cv2.imshow('Tello Camera', frame)

        cv2.waitKey(1)

    def showHorizon(self):
        frame = np.zeros([720, 960, 3])
        frame[:] = (0.5, 0.5, 0.5)

        bank_angle = self.tello_drone.get_roll()

        bank_angle = 90 - bank_angle

        pitch_angle =  - self.tello_drone.get_pitch()

        center_x = 360 + pitch_angle * 2
        center_y = 480

        print(bank_angle, pitch_angle)

        cv2.line(frame, (0, 360), (960, 360), (255, 0, 0), 3)

        length = 150

        x = round(center_x + length * math.cos(bank_angle * 3.14 / 180.0))
        y = round(center_y + length * math.sin(bank_angle * 3.14 / 180.0))

        cv2.line(frame, (center_y, center_x), (y, x), (0, 0, 255), 3)

        x = round(center_x + length * math.cos((180 + bank_angle) * 3.14 / 180.0))
        y = round(center_y + length * math.sin((180 + bank_angle) * 3.14 / 180.0))

        cv2.line(frame, (center_y, center_x), (y, x), (0, 0, 255), 3)

        cv2.imshow('Horizon', frame)

        cv2.waitKey(1)






    def __init__(self):
        self.kill_switch = self.TelloKillSwitch(self)
        self.kill_switch.start()

        self.stop_controller = Event()

        self.batt_status_printer = self.TelloTimer(1, self.stop_controller, self.getBatteryData)


        self.data_saver = self.TelloTimer(0.1, self.stop_controller, self.saveData)

        self.batt_check = self.TelloTimer(0.1, self.stop_controller, self.checkBattery)

        self.camera_stream = self.TelloTimer(1/30, self.stop_controller, self.showCameraStream)

        self.horizon = self.TelloTimer(1/30, self.stop_controller, self.showHorizon)


        self.tello_drone = tello.Tello()
        self.tello_drone.connect()

        self.tello_drone.streamon()
        self.frame_read = self.tello_drone.get_frame_read()

        # self.data_saver.start()
        self.batt_status_printer.start()
        # self.batt_check.start()

        self.camera_stream.start()

        self.horizon.start()

        self.pid_yaw = PID(0.65, 0.01, 0.4, setpoint=0, output_limits=(-100, 100))


        # self.takePicture()
        time.sleep(60)


        # cv2.imshow('Tello Camera', self.frame_read.frame)
        # time.sleep(3)

        # while True:
        #     # frame_read = cv2.resize(frame_read, (360, 240))


        # self.tello_drone.takeoff()

        #
        #
        # time.sleep(1)
        #
        # yaw = self.tello_drone.get_yaw()
        # print(yaw)
        # yaw_exp = yaw + 45
        #
        # yaw_off = yaw_exp - yaw
        #
        # while yaw_off > 2 or yaw_off < -2:
        #     rc_command = int(self.pid_yaw(yaw_off))
        #     if yaw_off > 1:
        #         self.tello_drone.send_rc_control(0, 0, 0, -rc_command)
        #     else:
        #         self.tello_drone.send_rc_control(0, 0, 0, rc_command)
        #     yaw = self.tello_drone.get_yaw()
        #     yaw_off = yaw_exp - yaw
        #     print("Yaw_exp: " + str(yaw_exp) + " Yaw_acc: " + str(yaw) + " Yaw_off: " + str(yaw_off) + " Cmd: " + str(rc_command))
        #
        # self.tello_drone.send_rc_control(0, 0, 0, 0)
        # time.sleep(2)
        #
        # self.tello_drone.land()

        self.tello_drone.end()

        self.stop_controller.set()


if __name__ == '__main__':
    # if os.geteuid() != 0:
    #     print('You need a root privileges!')
    # else:
    tc = TelloController()
