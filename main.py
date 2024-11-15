import cv2
import numpy as np
import mediapipe as mp
import gestures as g
import streamlit as st
import API_CONNECTOR
import time
import UI

# Initialize Mediapipe Hands model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
mp_drawing = mp.solutions.drawing_utils

# Variables for drawing
drawing = False  # Track if drawing
canvas = None
previous_x, previous_y = None, None
gesture_start_time = None  # For tracking the start of the index finger gesture
gesture_start_time2 = None  # For tracking the start of the 3-finger gesture

# Start webcam
cap = cv2.VideoCapture(0)

UI.mainIU()

# Streamlit layout
col1, col2 = st.columns([1, 1])
with col1:
    FRAME_WINDOW = st.image([])

with col2:
    saved_image_display = st.empty()  # Reserve space for dynamic updates



# Save drawing button (outside loop)
if st.button("Save Drawing", key="save_button"):
    if canvas is not None:
        cv2.imwrite("drawing_output.png", canvas)
        st.success("Drawing saved as 'drawing_output.png'")

# Streamlit loop for webcam capture and drawing
while True:
    success, img = cap.read()
    if not success:
        st.warning("Failed to capture video.")
        break

    # Initialize canvas if it hasn't been initialized
    if canvas is None:
        canvas = np.zeros_like(img)

    # Convert image to RGB for Mediapipe
    rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Process frame with Mediapipe
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks
            mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get coordinates of index finger tip
            index_finger_tip = hand_landmarks.landmark[8]
            h, w, c = img.shape
            x, y = int(index_finger_tip.x * w), int(index_finger_tip.y * h)

            # Handle drawing with index finger up
            if g.is_index_finger_up(hand_landmarks):
                if gesture_start_time is None:
                    gesture_start_time = time.time()
                elif time.time() - gesture_start_time >= 2:
                    if previous_x is None and previous_y is None:
                        previous_x, previous_y = x, y
                    cv2.line(canvas, (previous_x, previous_y), (x, y), (255, 255, 255), thickness=3)
                    previous_x, previous_y = x, y
            else:
                # Reset start time if index finger is not up anymore
                gesture_start_time = None
                previous_x, previous_y = None, None

            # Handle saving canvas with three fingers up
            if g.are_three_fingers_up(hand_landmarks):
                if gesture_start_time2 is None:
                    gesture_start_time2 = time.time()
                elif time.time() - gesture_start_time2 >= 3:
                    cv2.imwrite("drawing_output.png", canvas)
                    API_CONNECTOR.picGenarate()

                    saved_image_display.image("generated_image.png")
                    gesture_start_time2 = None  # Reset timer after saving
            else:
                # Reset start time if three fingers are not up anymore
                gesture_start_time2 = None

            # Handle clearing drawing when all fingers are up
            if g.are_all_fingers_down(hand_landmarks):
                canvas = np.zeros_like(img)

    # Combine canvas with image for display
    image_combination = cv2.addWeighted(img, 0.5, canvas, 1, 0)
    FRAME_WINDOW.image(image_combination, channels="BGR")

# Cleanup
cap.release()
cv2.destroyAllWindows()
