
import numpy as np
import cv2

def get_limits(color):
    c = np.uint8([[color]])  # Shape: (1, 1, 3)

    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    lowerLimit = np.array([
        max(0, int(hsvC[0][0][0]) - 10),
        100,
        100
    ], dtype=np.uint8)

    upperLimit = np.array([
        min(179, int(hsvC[0][0][0]) + 10),
        255,
        255
    ], dtype=np.uint8)

    return lowerLimit, upperLimit
