import mediapipe as mp
import cv2
import pandas as pd
import plotly.express as px
import numpy as np
from mathutils import Quaternion, Vector
import math

from addon.armature import Bone


class NoHandsDetectedException(Exception):
    def __init__(self):
        self.message = "No hands detected"
        super().__init__(self.message)


class HandDetect:
    def __init__(self):
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.8)

    def get_hand_data(self, frame):
        multi_hand_lms = self._find_hands(frame, raise_if_none=True)
        bones = []

        for hand_lms in multi_hand_lms:
            hand_lms = hand_lms.landmark
            for bone_pair in mp.solutions.hands.HAND_CONNECTIONS:
                cord_tuple = [hand_lms[i] for i in bone_pair]
                cord_tuple = tuple(map(
                    lambda lm: np.array(HandDetect.normalize_cords(frame, lm.x, lm.y, lm.z)), 
                    cord_tuple
                ))
                
                # bone length
                length = np.linalg.norm(cord_tuple[0] - cord_tuple[1])

                # translate vectors to origin
                cord_tuple_trans = tuple(map(
                    lambda x: x - cord_tuple[0], 
                    cord_tuple
                ))

                # bone rotation
                vec_before_rot = cord_tuple_trans[0] + np.array([length, 0, 0])
                vec_after_rot = cord_tuple_trans[1]

                quat_direction = np.cross(vec_before_rot, vec_after_rot)
                quat_rotation = math.pow(length, 4) + np.dot(vec_before_rot, vec_after_rot)

                # new bone
                bone = Bone(
                    "",
                    Vector(cord_tuple[0]),
                    Quaternion(quat_direction, quat_rotation), 
                    length
                )
                bones.append(bone)
                print(bone)
                
        return bones
    

    def show_hands(self, frame):
        multi_hand_lms = self._find_hands(frame)

        if multi_hand_lms is not None:
            for hand_lms in multi_hand_lms:
                mp.solutions.drawing_utils.draw_landmarks(self.frame, hand_lms, mp.solutions.hands.HAND_CONNECTIONS)

    def hand_graph(self, frame):
        hand_lm = self._find_hands(frame, raise_if_none=True)
        assert len(hand_lm) == 1, "Can only plot one hand"
        hand_lm = hand_lm[0]

        data_list = []
        for lm in hand_lm.landmark:
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

    def _find_hands(self, frame, raise_if_none=False):
        self.frame = frame
        frame_RGB = HandDetect.frame_to_RGB(frame)
        hands_detected = self.hands.process(frame_RGB)

        multi_hand_lms = getattr(hands_detected, 'multi_hand_landmarks', None)
        if multi_hand_lms is None and raise_if_none:
            raise NoHandsDetectedException
        
        return multi_hand_lms


    @staticmethod
    def normalize_cords(frame, x, y, z):
        h, w, _ = frame.shape
        return x * w, y * h, z * 2*w

    @staticmethod
    def frame_to_RGB(frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
