import mediapipe as mp

class HandTracker:
    def __init__(self, max_hands=1, detection_confidence=0.7):
        self.hands = mp.solutions.hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence)
        self.mp_draw = mp.solutions.drawing_utils

    def detect_hands(self, frame_rgb):
        return self.hands.process(frame_rgb)

    def get_landmarks(self, hand_landmarks, image_shape):
        h, w, _ = image_shape
        landmarks = []
        for lm in hand_landmarks.landmark:
            landmarks.append((int(lm.x * w), int(lm.y * h)))
        return landmarks

    def fingers_up(self, hand_landmarks):
        tips = [4, 8, 12, 16, 20]
        fingers = []

        if hand_landmarks.landmark[tips[0]].x < hand_landmarks.landmark[tips[0]-1].x:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1, 5):
            if hand_landmarks.landmark[tips[id]].y < hand_landmarks.landmark[tips[id]-2].y:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers
