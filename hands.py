import mediapipe as mp
import cv2


class HandDetect:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False,
                              max_num_hands=2,
                              min_detection_confidence=0.5,
                              min_tracking_confidence=0.5)
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, frame):
        frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_RGB)

        return results

    def show_hands(self, frame):
        if (multi_hand_lms := getattr(self.find_hands(frame), 'multi_hand_landmarks')) is not None:
            for hand_lms in multi_hand_lms:
                for id, lm in enumerate(hand_lms.landmark):
                    # print(id,lm)
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    # if id ==0:
                    cv2.circle(frame, (cx, cy), 3, (255, 0, 255), cv2.FILLED)

                self.mp_draw.draw_landmarks(frame, hand_lms, self.mp_hands.HAND_CONNECTIONS)
