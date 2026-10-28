import cv2
from projects_openccv.color_detection.util import get_limits
from PIL import Image

yellow = [0, 255, 255]

cap = cv2.VideoCapture(0)
while True:
    ret , frame = cap.read()
    # Convert the frame from BGR to HSV color space
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_bound, upper_bound =get_limits(color=yellow)

    mask = cv2.inRange(hsvImage, lower_bound, upper_bound)
    #image from array to PIL image
    mask_ = Image.fromarray(mask)
    bbox = mask_.getbbox()

    if bbox is not None:
        x1, y1, x2, y2 = bbox
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
    
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
     break
cap.release()
cv2.destroyAllWindows()