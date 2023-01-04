# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time
from djitellopy import Tello
import matplotlib.pyplot as plt
import pandas as pds
import csv
from csv import writer

# drone = Tello()  # tworzy instancję klasy Tello
# drone.connect()  # nawiązuje połączenie z dronem
#
# import calendar
# import time
#
# # Current GMT time in a tuple format
# current_GMT = time.gmtime()
#
# # ts stores timestamp
# ts = calendar.timegm(current_GMT)
#
# def append_list_as_row(file_name, list_of_elem):
#     # Open file in append mode
#     with open(file_name, 'a+', newline='') as write_obj:
#         # Create a writer object from csv module
#         csv_writer = writer(write_obj)
#         # Add contents of list as last row in the csv file
#         csv_writer.writerow(list_of_elem)
#
#
# append_list_as_row("tello_data_"+str(ts)+".csv",
#                    ["acc_x", "acc_y", "acc_z", "vel_x", "vel_y", "vel_z", "roll", "pitch", "yaw", "tof", "bat"])
#
#
#
# #  while True:
# #
# #     append_list_as_row("tello_data_"+str(ts)+".csv",
# #                        [drone.get_acceleration_x(), drone.get_acceleration_y(), drone.get_acceleration_z(),
# #                         drone.get_speed_x(), drone.get_speed_y(), drone.get_speed_z(),
# #                         drone.get_roll(), drone.get_pitch(), drone.get_yaw(),
# #                         drone.get_flight_time(), drone.get_battery()])
# #     print("writing data...")
# #     time.sleep(0.1)
# #
# # drone.end()  # zamyka połączenie, niszczy instancję klasy
print(__name__, 'dddd')