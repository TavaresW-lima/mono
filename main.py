# import os

# os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import cv2
import time
from detector import YoloDetector
from tracker import object_tracker
import serial
from controller import Controller
import util

detector = YoloDetector(model_name=None)
micro_controller = serial.Serial("COM4", 9600)
controller = Controller(device=micro_controller)
time.sleep(2)

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while cap.isOpened():
    succes, img = cap.read()

    start = time.perf_counter()

    results = detector.score_frame(img)
    img, detections = detector.plot_boxes(
        results, img, height=img.shape[0], width=img.shape[1], confidence=0.5
    )

    tracks = object_tracker.update_tracks(
        detections, frame=img
    )  # bbs expected to be a list of detections, each in tuples of ( [left,top,w,h], confidence, detection_class )

    mainTrack = None
    for track in tracks:
        if track.is_confirmed():
            mainTrack = track
            break

    bbox = None
    if mainTrack != None:
        track_id = mainTrack.track_id
        ltrb = mainTrack.to_ltrb()

        bbox = ltrb

        cv2.rectangle(
            img,
            (int(bbox[0]), int(bbox[1])),
            (int(bbox[2]), int(bbox[3])),
            (0, 0, 255),
            2,
        )
        cv2.putText(
            img,
            "ID: " + str(track_id),
            (int(bbox[0]), int(bbox[1] - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 0),
            2,
        )
        senX, velX, senY, velY = util.verifyTrackDisplacement(*bbox)
        if velX > 0 or velY > 0:
            controller.move((senX, velX, senY, velY))
            print(
                f"Moved: {'<-' if senX == 1 else '->'} {velX}, {'up' if senY == 0 else 'down'} {velY}"
            )

    end = time.perf_counter()
    totalTime = end - start
    fps = 1 / totalTime

    util.drawRulers(img)
    cv2.putText(
        img, f"FPS: {int(fps)}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2
    )
    cv2.imshow("img", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break


# Release and destroy all windows before termination
cap.release()

cv2.destroyAllWindows()
