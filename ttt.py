import cv2
import numpy as np
import mediapipe as mp
import streamlit as st
from PIL import Image
import gestures as g  # Assuming you have this module for gesture recognition

# Initialize Mediapipe Hands model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
mp_drawing = mp.solutions.drawing_utils

# Variables for drawing
drawing = False  # Track if drawing
canvas = None
previous_x, previous_y = None, None


# Function to get the frame with drawing
def get_hand_drawing_frame():
    cap = cv2.VideoCapture(0)

    # Create a white canvas for drawing
    global canvas, previous_x, previous_y
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # Initialize canvas
        if canvas is None:
            canvas = np.zeros_like(frame)

        # Process frame with Mediapipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
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

                # Check if index finger is up (drawing mode)
                if g.is_index_finger_up(hand_landmarks):
                    if previous_x is None and previous_y is None:
                        previous_x, previous_y = x, y
                    # Draw line on canvas
                    cv2.line(canvas, (previous_x, previous_y), (x, y), (255, 255, 255), thickness=3)
                    previous_x, previous_y = x, y

                # Check if three fingers are up (delete)
                elif g.are_three_fingers_up(hand_landmarks):
                    # Clear the canvas or trigger any other action
                    canvas = np.zeros_like(frame)

                # Reset drawing coordinates when finger is lifted
                else:
                    previous_x, previous_y = None, None

        # Merge canvas with frame
        frame = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)
        frame = cv2.resize(frame, (640, 480))  # Or any lower resolution that works for you

        # Convert frame to RGB for Streamlit
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert to PIL Image (for Streamlit)
        img = Image.fromarray(rgb_frame)

        # Display in Streamlit (instead of cv2.imshow)
        cap.release()
        return img

    cap.release()
    return None


def main():
    # Set page configuration
    st.set_page_config(page_title="Creativity at Your Fingertips", layout="wide")

    # Header
    st.markdown("""<div style="text-align: center;">
            <h1>Creativity at Your Fingertips<br> Unlocking Imagination with Every Gesture</h1>
        </div>""", unsafe_allow_html=True)

    # Middle Section
    col1, col2 = st.columns(2)

    # Block-1 (input cam and output pic)
    with col1:
        st.markdown('<div style="text-align: center;"><div class="card-1"></div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div style="text-align: center;"><div class="card-1"></div></div>', unsafe_allow_html=True)

    # Block-2 (Instructions)
    st.markdown("""
        <div class="block-2">
            <p>
            <b>Instructions:</b>
            <ul>
                <li>Index Finger : Use to draw lines</li>
                <li>Index Finger + Middle Finger : To idle and move fingers across display</li>
                <li>Index Finger + Middle Finger + Ring Finger : Delete the drawing</li>
                <li>All Fingers : To post picture</li>
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("<div class='footer'></div>", unsafe_allow_html=True)

    # Custom CSS for styling
    st.markdown("""
        <style>
        * {
            font-family: 'Ubuntu', sans-serif;
            background-color: #000000;
            color : white;
        }
        h1 {
            text-align: center;
        }
        li {
            margin-bottom: 10px;
        }
        .block-1 {
            display: flex;
            gap: 20px;
            margin: 20px 0;
            justify-content: center;
            align-items: center;
        }
        .card-1 {
            background-color: #444444;
            padding: 20px;
            border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Streamlit container for the webcam feed
    st.markdown("### Live Hand Gesture Drawing")
    image_placeholder = st.empty()

    # Display webcam feed with drawing on it
    while True:
        img = get_hand_drawing_frame()  # Get the frame from OpenCV with drawing
        if img:
            image_placeholder.image(img, channels="RGB", use_container_width=True)
        else:
            break

    st.write("End of Stream")

if __name__ == "__main__":
    main()
