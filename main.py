import cv2
import numpy as np
import mediapipe as mp

# Initialize Mediapipe Hands model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
mp_drawing = mp.solutions.drawing_utils

# Variables for drawing
drawing = False  # Track if drawing
canvas = None  # Drawing canvas
previous_x, previous_y = None, None

# Start webcam
cap = cv2.VideoCapture(0)

def are_all_fingers_up(hand_landmarks):
    # Check each finger by comparing the y-coordinates of the fingertip and the lower joint
    thumb_up = hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x  # Thumb direction differs
    index_up = hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y
    middle_up = hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y
    ring_up = hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y
    pinky_up = hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y

    # Return True if all fingers are up
    return thumb_up and index_up and middle_up and ring_up and pinky_up


while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Initialize canvas
    if canvas is None:
        canvas = np.zeros_like(frame)

    # Convert to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process frame with Mediapipe
    results = hands.process(rgb_frame)

    # Draw hands and track index finger
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks on frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get coordinates of index finger tip (landmark 8)
            index_finger_tip = hand_landmarks.landmark[8]
            h, w, c = frame.shape
            x, y = int(index_finger_tip.x * w), int(index_finger_tip.y * h)

            # Check if index finger is down (drawing mode)
            if hand_landmarks.landmark[12].y > hand_landmarks.landmark[8].y:  # Check middle finger position
                if previous_x is None and previous_y is None:
                    previous_x, previous_y = x, y
                # Draw line on canvas
                cv2.line(canvas, (previous_x, previous_y), (x, y), (255, 0, 0), thickness=3)
                previous_x, previous_y = x, y

            elif are_all_fingers_up(hand_landmarks):
                # Clear the canvas or trigger any other action
                canvas = np.zeros_like(frame)  # Example action: clear canvas

            else:
                # Reset drawing coordinates when finger is lifted
                previous_x, previous_y = None, None

    # Merge canvas with frame
    frame = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)

    # Display the frame
    cv2.imshow("Hand Drawing", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
