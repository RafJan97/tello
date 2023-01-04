from djitellopy import tello
from threading import Thread, Event
import keyboard
import calendar
import time
from csv import writer
import csv


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

    def checkBattery(self):
        if self.tello_drone.get_battery() < 20:
            print("Battery Low! ", self.tello_drone.get_battery())

    def __init__(self):
        self.kill_switch = self.TelloKillSwitch(self)
        self.kill_switch.start()

        self.stop_controller = Event()

        self.batt_status_printer = self.TelloTimer(1, self.stop_controller, self.getBatteryData)
        self.batt_status_printer.start()

        self.batt_check = self.TelloTimer(0.1, self.stop_controller, self.checkBattery)
        self.batt_check.start()

        self.tello_drone = tello.Tello()
        self.tello_drone.connect()

        self.tello_drone.takeoff()
        time.sleep(1)

        yaw = self.tello_drone.get_yaw()
        print(yaw)
        yaw_exp = yaw + 45

        while yaw < yaw_exp -1 or yaw > yaw_exp +1:
            if yaw > yaw_exp +1:
                self.tello_drone.send_rc_control(0, 0, 0, -20)
            else:
                self.tello_drone.send_rc_control(0, 0, 0, 20)
            yaw = self.tello_drone.get_yaw()
            print(yaw)

        self.tello_drone.land()

        self.tello_drone.end()

        self.stop_controller.set()


if __name__ == '__main__':
    # if os.geteuid() != 0:
    #     print('You need a root privileges!')
    # else:
    tc = TelloController()
