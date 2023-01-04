import cv2
import numpy as np


import math



frame = np.zeros([720, 960, 3])
frame[:] = (0.5, 0.5, 0.5)

bank_angle = 45

bank_angle = 90 - bank_angle

pitch_angle = 10

center_x = 360 + pitch_angle*5
center_y = 480 + pitch_angle

print(bank_angle, pitch_angle)

cv2.line(frame, (0, 360), (960, 360), (255, 0, 0), 3)

length = 150


x =  round(center_x + length * math.cos(bank_angle * 3.14 / 180.0))
y =  round(center_y + length * math.sin(bank_angle * 3.14 / 180.0))

cv2.line(frame, (center_y, center_x), (y, x), (0, 0, 255), 3)

x =  round(center_x + length * math.cos((180 + bank_angle) * 3.14 / 180.0))
y =  round(center_y + length * math.sin((180 + bank_angle) * 3.14 / 180.0))

cv2.line(frame, (center_y, center_x), (y, x), (0, 0, 255), 3)


cv2.imshow('Horizon', frame)



cv2.waitKey(0)
cv2.destroyAllWindows()