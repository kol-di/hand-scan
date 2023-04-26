import cv2
import time

from detector.hands import HandDetect


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
        hand_detect.find_hands(frame, show=True)
        cv2.putText(frame, f'FPS:{int(fps)}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('video feed', frame)

        # stop display
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # plot
        if cv2.waitKey(1) & 0xFF == ord(' '):
            hand_detect.find_hands(frame, show=False, plot=True)
            break

    cap.release()
    cv2.destroyAllWindows()
