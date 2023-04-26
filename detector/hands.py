import mediapipe as mp
import cv2
import pandas as pd
import plotly.express as px


class HandDetect:
    def __init__(self):
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.8)

    def find_hands(self, frame, show, plot=False):
        self.frame = frame
        frame_RGB = HandDetect.frame_to_RGB(frame)
        hands_detected = self.hands.process(frame_RGB)

        if (multi_hand_lms := getattr(hands_detected, 'multi_hand_landmarks')) is not None:
            if show:
                self._show_hands(multi_hand_lms)
            if plot:
                self._hand_graph(multi_hand_lms)

    def _show_hands(self, multi_hand_lms):
        for hand_lms in multi_hand_lms:
            mp.solutions.drawing_utils.draw_landmarks(self.frame, hand_lms, mp.solutions.hands.HAND_CONNECTIONS)

    def _hand_graph(self, multi_hand_lms):
        assert len(multi_hand_lms) == 1, "Can only plot one hand"

        data_list = []
        for lm in multi_hand_lms[0].landmark:
            data_list.append(
                list(HandDetect.normalize_cords(self.frame, lm.x, lm.y, lm.z)))
        points_df = pd.DataFrame(data_list, columns=['x', 'y', 'z'])

        x, y, z, indices = [], [], [], []
        for ind, points in enumerate(mp.solutions.hands.HAND_CONNECTIONS):
            for point in points:
                point_row = points_df.iloc[point,:]
                x.append(point_row['x'])
                y.append(point_row['y'])
                z.append(point_row['z'])
                indices.append(ind)
        lines_df = pd.DataFrame({'x': x, 'y': y, 'z': z, 'ind': indices})

        fig = px.line_3d(lines_df, x='x', y='y', z='z', color='ind')
        fig.show()


    @staticmethod
    def normalize_cords(frame, x, y, z):
        h, w, c = frame.shape
        return x * w, y * h, z * 2*w

    @staticmethod
    def frame_to_RGB(frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
