
import cv2
import numpy as np


framewidth = 640
frameheight = 480

cap = cv2.VideoCapture(0)
cap.set(3, framewidth)
cap.set(4, frameheight)
cap.set(10, 150)



def preProcessing(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)

    imgCanny = cv2.Canny(imgBlur, 200, 200)

    kernel = np.ones((5, 5), np.uint8)

    imgDial = cv2.dilate(imgCanny, kernel, iterations=2)

    imgErod = cv2.erode(imgDial, kernel, iterations=1)

    return imgErod



def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))

    newPoints = np.zeros((4, 2), dtype=np.float32)

    add = myPoints.sum(axis=1)
    diff = np.diff(myPoints, axis=1)

    newPoints[0] = myPoints[np.argmin(add)]  
    newPoints[1] = myPoints[np.argmin(diff)]  
    newPoints[2] = myPoints[np.argmax(diff)]  
    newPoints[3] = myPoints[np.argmax(add)]   

    return newPoints



def getContours(img):
    biggest = np.array([])
    maxarea = 0

    contours, hierarchy = cv2.findContours(
        img,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_NONE
    )

    for cnt in contours:

        area = cv2.contourArea(cnt)

        if area > 5000:

            peri = cv2.arcLength(cnt, True)

            approx = cv2.approxPolyDP(
                cnt,
                0.02 * peri,
                True
            )

            # Keep the largest quadrilateral
            if len(approx) == 4 and area > maxarea:
                biggest = approx
                maxarea = area

    # Draw the detected quadrilateral
    if biggest.size != 0:
        cv2.drawContours(
            imgContour,
            [biggest],
            -1,
            (255, 0, 0),
            3
        )

    return biggest



def getWarp(img, biggest):

    pts1 = reorder(biggest)

    pts2 = np.float32([
        [0, 0],
        [framewidth, 0],
        [0, frameheight],
        [framewidth, frameheight]
    ])

    matrix = cv2.getPerspectiveTransform(
        pts1,
        pts2
    )

    imgOutput = cv2.warpPerspective(
        img,
        matrix,
        (framewidth, frameheight)
    )

    return imgOutput



while True:

    success, img = cap.read()

    if not success:
        print("Failed to capture image from camera.")
        break

    img = cv2.resize(img, (framewidth, frameheight))

    # Copy original image for drawing contours
    imgContour = img.copy()


    imgthresh = preProcessing(img)

    # Find largest quadrilateral
    biggest = getContours(imgthresh)

  
    if biggest.size != 0:

        warpedimg = getWarp(img, biggest)

        cv2.imshow("warped", warpedimg)

    else:
        cv2.imshow("result", img)


    cv2.imshow("Original", img)
    cv2.imshow("Preprocessed", imgthresh)
    cv2.imshow("Contours", imgContour)

 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cap.release()
cv2.destroyAllWindows()
