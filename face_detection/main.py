import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)

# Initialize face detection once
mp_face_detection = mp.solutions.face_detection

with mp_face_detection.FaceDetection(
    model_selection=0,
    min_detection_confidence=0.5
) as face_detection:

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to capture frame")
            break

        # Convert BGR to RGB because MediaPipe expects RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces
        results = face_detection.process(rgb_frame)

        if results.detections:
            for detection in results.detections:
                location_data = detection.location_data
                bbox = location_data.relative_bounding_box
                # Get frame dimensions
                H, W, _ = frame.shape

        # Convert normalized coordinates to pixels
                x1 = int(bbox.xmin * W)
                y1 = int(bbox.ymin * H)

                w = int(bbox.width * W)
                h = int(bbox.height * H)

        # Keep coordinates inside the image
                x1 = max(0, x1)
                y1 = max(0, y1)

                x2 = min(W, x1 + w)
                y2 = min(H, y1 + h)

        # Blur the detected face
                face_region = frame[y1:y2, x1:x2]

                if face_region.size > 0:
                   frame[y1:y2, x1:x2] = cv2.blur(
                  face_region, (50, 50)
                     )

                #mp.solutions.drawing_utils.draw_detection(
                 #   frame, detection
               # )

        cv2.imshow("Face Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()