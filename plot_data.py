# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time
import calendar
from djitellopy import Tello
from csv import writer
import matplotlib.pyplot as plt
import random

drone = Tello()  # tworzy instancję klasy Tello
drone.connect()  # nawiązuje połączenie z dronem


while True:

    ax1 = plt.subplot(311)
    plt.plot(t, s1)
    plt.tick_params('x', labelsize=6)

    # share x only
    ax2 = plt.subplot(312, sharex=ax1)
    plt.plot(t, s2)
    # make these tick labels invisible
    plt.tick_params('x', labelbottom=False)

    # share x and y
    ax3 = plt.subplot(313, sharex=ax1, sharey=ax1)
    plt.plot(t, s3)
    plt.xlim(0.01, 5.0)
    plt.show()

    print("writing data...")
    time.sleep(0.1)

drone.end()  # zamyka połączenie, niszczy instancję klasy




x = []
y = []

plt.plot(x, y)

cnt = 0
while True:
    x.append(cnt)
    y.append(random.randint(0, 100))

    plt.gca().lines[0].set_xdata(x)
    plt.gca().lines[0].set_ydata(y)
    plt.gca().relim()
    plt.gca().autoscale_view()
    plt.pause(0.1)

    cnt += 1

    if cnt > 20:
        cnt = 0
        y = []
        x = []
        plt.pause(2.0)


