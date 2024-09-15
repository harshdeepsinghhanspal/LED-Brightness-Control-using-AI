import cv2
import mediapipe as mp
import serial
import time

# Initialize serial communication
arduino = serial.Serial('COM9', 9600)  # Change 'COM3' to your Arduino port
time.sleep(2)  # Wait for the serial connection to initialize

# Initialize MediaPipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Capture video from webcam
cap = cv2.VideoCapture(0)

def calculate_distance(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

while True:
    success, img = cap.read()
    if not success:
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the coordinates of the tip of the index finger and thumb
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

            # Convert normalized coordinates to pixel values
            h, w, _ = img.shape
            index_finger_tip = (int(index_finger_tip.x * w), int(index_finger_tip.y * h))
            thumb_tip = (int(thumb_tip.x * w), int(thumb_tip.y * h))

            # Calculate the distance between the index finger tip and thumb tip
            distance = calculate_distance(index_finger_tip, thumb_tip)

            # Map the distance to a brightness value (0-255)
            brightness = int(min(max(distance, 0), 255))

            # Send the brightness value to the Arduino
            arduino.write(bytes([brightness]))

            # Display the distance on the image
            cv2.putText(img, f'Brightness: {brightness}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow('Hand Tracking', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
