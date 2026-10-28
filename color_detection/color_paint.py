
import cv2
import numpy as np
from util import get_limits

# BGR colors
myColors = [
    [0, 255, 255],    # Yellow
    [0, 255, 0],      # Green
    [255, 0, 255]     # Purple
]

def findColor(img, color):
    hsvImage = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_bound, upper_bound = get_limits(color=color)
    mask = cv2.inRange(hsvImage, lower_bound, upper_bound)

    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    if contours:
        largest = max(contours, key=cv2.contourArea)
#noise filtering using an area threshold.
        if cv2.contourArea(largest) > 500:
            M = cv2.moments(largest)

            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                return cx, cy

    return None


cap = cv2.VideoCapture(0)

canvas = None
previous_point = None
current_color = None

while True:
    ret, frame = cap.read()

    if not ret:
        break

    if canvas is None:
        canvas = np.zeros_like(frame)

    for color in myColors:
        center = findColor(frame, color)

        if center is not None:
            x, y = center

            if previous_point is not None and current_color == color:
                cv2.line(canvas, previous_point, (x, y), color, 8)

            previous_point = (x, y)
            current_color = color

            cv2.circle(frame, (x, y), 10, color, cv2.FILLED)
            break

    else:
        previous_point = None
        current_color = None

    result = cv2.addWeighted(frame, 1, canvas, 1, 0)

    cv2.imshow("Virtual Painter", result)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

    if key == ord('c'):
        canvas[:] = 0

cap.release()
cv2.destroyAllWindows()
