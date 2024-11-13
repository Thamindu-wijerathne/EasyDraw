import cv2
import numpy as np
import mediapipe as mp
import gestures as g
import UI

# Initialize Mediapipe Hands model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
mp_drawing = mp.solutions.drawing_utils

# Variables for drawing
drawing = False  # Track if drawing
canvas = None
previous_x, previous_y = None, None

# Start webcam
cap = cv2.VideoCapture(0)

# Create a white canvas for drawing
# canvas_width, canvas_height = 640, 480
# canvas = np.ones((canvas_height, canvas_width, 3), dtype=np.uint8) * 255  # White background

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
            if g.is_index_finger_up(hand_landmarks):  # Check middle finger position
                if previous_x is None and previous_y is None:
                    previous_x, previous_y = x, y
                # Draw line on canvas
                cv2.line(canvas, (previous_x, previous_y), (x, y), (255, 255, 255), thickness=3)
                previous_x, previous_y = x, y

            # Check if index middle ring finger is up (delete)
            elif g.are_three_fingers_up(hand_landmarks):
                # Clear the canvas or trigger any other action
                canvas = np.zeros_like(frame)  # Example action: clear canvas

            # Check if all fingers are up (save)
            elif g.are_all_fingers_up(hand_landmarks):
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

    # Save drawing when 's' is pressed
    if cv2.waitKey(1) & 0xFF == ord('s'):
        # Save the canvas as an image
        cv2.imwrite("drawing_output.png", canvas)
        print("Drawing saved as 'drawing_output.png'")

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Cleanup
cap.release()
cv2.destroyAllWindows()
