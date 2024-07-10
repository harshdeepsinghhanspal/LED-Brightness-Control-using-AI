import cv2
import serial
import mediapipe as mp

# Initialize serial communication with Arduino
arduino = serial.Serial('COM9', 9600)  # Replace 'COM9' with your Arduino port


def write_to_arduino(value):
    arduino.write(bytes(value, 'utf-8'))


# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Start video capture
cap = cv2.VideoCapture(0)

with mp_face_detection.FaceDetection(
        model_selection=0, min_detection_confidence=0.5) as face_detection:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the BGR image to RGB.
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the image and detect faces.
        results = face_detection.process(frame_rgb)

        # Draw face detections of each face.
        if results.detections:
            write_to_arduino('1')  # Send '1' to Arduino to turn on the LED
            for detection in results.detections:
                mp_drawing.draw_detection(frame, detection)
        else:
            write_to_arduino('0')  # Send '0' to Arduino to turn off the LED

        # Display the output
        cv2.imshow('Face Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
