{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "838697cf",
   "metadata": {},
   "outputs": [],
   "source": [
    "import cv2\n",
    "import time\n",
    "import numpy as np"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "6ddbacf6",
   "metadata": {},
   "outputs": [],
   "source": [
    "def get_limits(color):\n",
    "    c = np.uint8([[color]])\n",
    "\n",
    "    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)\n",
    "\n",
    "    lowerLimit = np.array([\n",
    "        max(0, int(hsvC[0][0][0]) - 10),\n",
    "        100,\n",
    "        100\n",
    "    ], dtype=np.uint8)\n",
    "\n",
    "    upperLimit = np.array([\n",
    "        min(179, int(hsvC[0][0][0]) + 10),\n",
    "        255,\n",
    "        255\n",
    "    ], dtype=np.uint8)\n",
    "\n",
    "    return lowerLimit, upperLimit"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "943b6083",
   "metadata": {},
   "outputs": [],
   "source": [
    "myColors = [\n",
    "    [0, 255, 255],    # Yellow\n",
    "    [0, 255, 0],      # Green\n",
    "    [255, 0, 255]     # Purple\n",
    "]\n",
    "\n",
    "drawColors = myColors"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "857ca46b",
   "metadata": {},
   "outputs": [],
   "source": [
    "def findColor(img, color):\n",
    "\n",
    "    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)\n",
    "\n",
    "    lowerLimit, upperLimit = get_limits(color)\n",
    "\n",
    "    mask = cv2.inRange(imgHsv, lowerLimit, upperLimit)\n",
    "\n",
    "    contours, _ = cv2.findContours(\n",
    "        mask,\n",
    "        cv2.RETR_EXTERNAL,\n",
    "        cv2.CHAIN_APPROX_SIMPLE\n",
    "    )\n",
    "\n",
    "    if contours:\n",
    "        largest = max(contours, key=cv2.contourArea)\n",
    "\n",
    "        if cv2.contourArea(largest) > 500:\n",
    "\n",
    "            M = cv2.moments(largest)\n",
    "\n",
    "            if M[\"m00\"] != 0:\n",
    "                cx = int(M[\"m10\"] / M[\"m00\"])\n",
    "                cy = int(M[\"m01\"] / M[\"m00\"])\n",
    "\n",
    "                return cx, cy\n",
    "\n",
    "    return None"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "46630d45",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Opened: True\n"
     ]
    }
   ],
   "source": [
    "cap = cv2.VideoCapture(0, cv2.CAP_V4L2)\n",
    "\n",
    "cap.set(cv2.CAP_PROP_FOURCC,\n",
    "        cv2.VideoWriter_fourcc(*'MJPG'))\n",
    "\n",
    "cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)\n",
    "cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)\n",
    "cap.set(cv2.CAP_PROP_FPS, 15)\n",
    "cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)\n",
    "\n",
    "print(\"Opened:\", cap.isOpened())\n",
    "\n",
    "canvas = np.zeros((480, 640, 3), dtype=np.uint8)\n",
    "\n",
    "previous_point = None\n",
    "current_color = None\n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "663009d5",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "QFontDatabase: Cannot find font directory /home/elite_computer/robotics/Python_Projects/.venv/lib/python3.12/site-packages/cv2/qt/fonts.\n",
      "Note that Qt no longer ships fonts. Deploy some (from https://dejavu-fonts.github.io/ for example) or switch to fontconfig.\n",
      "QFontDatabase: Cannot find font directory /home/elite_computer/robotics/Python_Projects/.venv/lib/python3.12/site-packages/cv2/qt/fonts.\n",
      "Note that Qt no longer ships fonts. Deploy some (from https://dejavu-fonts.github.io/ for example) or switch to fontconfig.\n",
      "QFontDatabase: Cannot find font directory /home/elite_computer/robotics/Python_Projects/.venv/lib/python3.12/site-packages/cv2/qt/fonts.\n",
      "Note that Qt no longer ships fonts. Deploy some (from https://dejavu-fonts.github.io/ for example) or switch to fontconfig.\n",
      "QFontDatabase: Cannot find font directory /home/elite_computer/robotics/Python_Projects/.venv/lib/python3.12/site-packages/cv2/qt/fonts.\n",
      "Note that Qt no longer ships fonts. Deploy some (from https://dejavu-fonts.github.io/ for example) or switch to fontconfig.\n",
      "QFontDatabase: Cannot find font directory /home/elite_computer/robotics/Python_Projects/.venv/lib/python3.12/site-packages/cv2/qt/fonts.\n",
      "Note that Qt no longer ships fonts. Deploy some (from https://dejavu-fonts.github.io/ for example) or switch to fontconfig.\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Frame capture failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "[ WARN:0@49.392] global cap_v4l.cpp:1049 tryIoctl VIDEOIO(V4L2:/dev/video0): select() timeout.\n"
     ]
    }
   ],
   "source": [
    "while cap.isOpened():\n",
    "\n",
    "    ret, frame = cap.read()\n",
    "\n",
    "    if not ret:\n",
    "        print(\"Frame capture failed\")\n",
    "        break\n",
    "\n",
    "    for color in myColors:\n",
    "\n",
    "        center = findColor(frame, color)\n",
    "\n",
    "        if center is not None:\n",
    "\n",
    "            x, y = center\n",
    "\n",
    "            if previous_point is not None and current_color == color:\n",
    "                cv2.line(\n",
    "                    canvas,\n",
    "                    previous_point,\n",
    "                    (x, y),\n",
    "                    color,\n",
    "                    8\n",
    "                )\n",
    "\n",
    "            previous_point = (x, y)\n",
    "            current_color = color\n",
    "\n",
    "            cv2.circle(frame, (x, y), 10, color, cv2.FILLED)\n",
    "\n",
    "            break\n",
    "\n",
    "    else:\n",
    "        previous_point = None\n",
    "        current_color = None\n",
    "\n",
    "    result = cv2.addWeighted(frame, 1, canvas, 1, 0)\n",
    "\n",
    "    cv2.imshow(\"Virtual Painter\", result)\n",
    "\n",
    "    key = cv2.waitKey(1) & 0xFF\n",
    "\n",
    "    if key == 27:\n",
    "        break\n",
    "\n",
    "    if key == ord('c'):\n",
    "        canvas[:] = 0"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "9858c306",
   "metadata": {},
   "outputs": [],
   "source": [
    "cap.release()\n",
    "cv2.destroyAllWindows()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "1e928df1",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": ".venv (3.12.3)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
