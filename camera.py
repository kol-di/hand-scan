import cv2
import time


def display():
    cap = cv2.VideoCapture(0)

    start_time = 0
    while True:
        success, frame = cap.read()

        # calculate fps
        end_time = time.time()
        fps = 1 / (end_time - start_time)
        start_time = end_time

        # display frame
        cv2.putText(frame, f'FPS:{int(fps)}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('video feed', frame)

        # stop display
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
