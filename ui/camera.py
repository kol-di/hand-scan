import cv2
import time
import bpy

from detector.hands import HandDetect, NoHandsDetectedException
from addon.armature import create_hand_armature


def capture_video(source):
   cap = cv2.VideoCapture(source) 
   if cap is None or not cap.isOpened():
       raise Exception('Warning: unable to open video source: ', source)
   else:
       return cap


def display():
    cap = capture_video(0)

    hand_detect = HandDetect()

    start_time = 0
    while True:
        success, frame = cap.read()

        # calculate fps
        end_time = time.time()
        fps = 1 / (end_time - start_time)
        start_time = end_time

        # display frame
        hand_detect.show_hands(frame)
        cv2.putText(frame, f'FPS:{int(fps)}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('video feed', frame)

        pressed_key = cv2.waitKey(1) & 0xFF

        # stop display
        if pressed_key == ord('q'):
            break

        # plot
        if pressed_key == ord(' '):
            try:
                hand_detect.hand_graph(frame)
                break
            except NoHandsDetectedException:
                pass

        # save hand data
        if pressed_key == ord('s'):
            try:
                hand_data = hand_detect.get_hand_data(frame)
                context = bpy.context
                create_hand_armature(context, hand_data)
                break
            except NoHandsDetectedException:
                pass

    cap.release()
    cv2.destroyAllWindows()
