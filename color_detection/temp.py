import cv2

backends = {
    "MSMF": cv2.CAP_MSMF,
    "DSHOW": cv2.CAP_DSHOW
}

for name, backend in backends.items():
    print(f"\nTesting {name}...")

    for index in range(4):
        cap = cv2.VideoCapture(index, backend)

        print(f"Camera {index}: {cap.isOpened()}")

        if cap.isOpened():
            ret, frame = cap.read()
            print("Frame received:", ret)

        cap.release()