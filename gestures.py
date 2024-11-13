def are_all_fingers_up(hand_landmarks):
    # Check each finger by comparing the y-coordinates of the fingertip and the lower joint
    thumb_up = hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x  # Thumb direction differs
    index_up = hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y
    middle_up = hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y
    ring_up = hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y
    pinky_up = hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y

    # Return True if all fingers are up
    return thumb_up and index_up and middle_up and ring_up and pinky_up

def is_index_finger_up(hand_landmarks):
    index_up = hand_landmarks.landmark[12].y > hand_landmarks.landmark[8].y

    return index_up

def are_three_fingers_up(hand_landmarks):
    # Check each finger by comparing the y-coordinates of the fingertip and the lower joint
    index_up = hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y
    middle_up = hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y
    ring_up = hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y

    # Return True if all three specified fingers are up
    return index_up and middle_up and ring_up
