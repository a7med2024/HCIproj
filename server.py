import mediapipe as mp 
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import time 
from dollarpy import Recognizer, Template, Point
import bluetooth

import socket
soc = socket.socket()
hostname="localhost"# 127.0.0.1 #0.0.0.0
port=64252
soc.bind((hostname,port))
soc.listen(5)
conn, addr = soc.accept()
print("Client connected")

print("Detecting Bluetooth Devices")
nearby_devices = bluetooth.discover_devices(lookup_names=True)
print("found %d devices" % len(nearby_devices))

for addr, name in nearby_devices:
     print(" %s - %s" % (addr, name))
mp_drawing = mp.solutions.drawing_utils 
mp_drawing_styles = mp.solutions.drawing_styles

mp_holistic = mp.solutions.holistic 

def print_result(result: mp.tasks.vision.GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    #print('gesture recognition result: {}'.format(result.gestures))
    
    if (len(result.gestures) > 0):
        top_gesture = result.gestures[0][0].category_name
        conn.send(top_gesture.encode())


#recognizer = Recognizer(templates)
base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
options = vision.GestureRecognizerOptions(base_options=base_options,
    running_mode=mp.tasks.vision.RunningMode.LIVE_STREAM,
    result_callback=print_result)
recognizer = vision.GestureRecognizer.create_from_options(options)

def startDetecting(label):
    cap = cv2.VideoCapture(0) #web cam =0, else enter filename
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while cap.isOpened():
            ret, frame = cap.read()
            # Recolor Feed
            if ret==True:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False        
                # Make Detections
                results = holistic.process(image)
                # print(results.face_landmarks)

                # Recolor image back to BGR for rendering
                image.flags.writeable = True   
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # Drawing on Frame (You can remove it)
                # 2. Right hand
                mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
                # 3. Left Hand
                mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
                # 4. Pose Detections
                #mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
                recognizer.recognize_async(mp.Image(image_format=mp.ImageFormat.SRGB, data=frame), time.perf_counter_ns())

                cv2.imshow(label, image)
            else :
                cap.release()
                cv2.destroyAllWindows()
                cv2.waitKey(100)
                break

            if cv2.waitKey(10) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                cv2.waitKey(100)
                break
    cap.release()
    cv2.destroyAllWindows()

startDetecting("Reading Gestures")
# for adding gesu
#import pickle
#with open("data.model", "wb") as fp:
#    pickle.dump(templates, fp)
