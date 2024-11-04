import mediapipe as mp 
import cv2
import pickle
import time 
from dollarpy import Recognizer, Template, Point

#load gestures
templates=[] 
with open("data.model", "rb") as fp:  
    templates = pickle.load(fp)

mp_drawing = mp.solutions.drawing_utils 
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic 

def getPoints(label):
    cap = cv2.VideoCapture(0) #web cam =0, else enter filename
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        points = []
        left_shoulder=[]
        right_shoulder=[]
        left_elbos=[]
        right_elbos=[]
        left_wirst=[]
        right_wrist=[]
        left_pinky=[]
        right_pinky=[]
        left_index=[]
        right_index=[]
        left_hip=[]
        right_hip=[]        
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
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

                # Export coordinates
                try:
                    # add points of wrist , elbow and shoulder
                    left_shoulder.append(Point(results.pose_landmarks.landmark[11].x,results.pose_landmarks.landmark[11].y,1))
                    right_shoulder.append(Point(results.pose_landmarks.landmark[12].x,results.pose_landmarks.landmark[12].y,2))
                    left_elbos.append(Point(results.pose_landmarks.landmark[13].x,results.pose_landmarks.landmark[13].y,3))
                    right_elbos.append(Point(results.pose_landmarks.landmark[14].x,results.pose_landmarks.landmark[14].y,4))
                    left_wirst.append(Point(results.pose_landmarks.landmark[15].x,results.pose_landmarks.landmark[15].y,5))
                    right_wrist.append(Point(results.pose_landmarks.landmark[16].x,results.pose_landmarks.landmark[16].y,6))
                    left_pinky.append(Point(results.pose_landmarks.landmark[17].x,results.pose_landmarks.landmark[17].y,7))
                    right_pinky.append(Point(results.pose_landmarks.landmark[18].x,results.pose_landmarks.landmark[18].y,8))
                    left_index.append(Point(results.pose_landmarks.landmark[19].x,results.pose_landmarks.landmark[19].y,9))
                    right_index.append(Point(results.pose_landmarks.landmark[20].x,results.pose_landmarks.landmark[20].y,10))
                    left_hip.append(Point(results.pose_landmarks.landmark[23].x,results.pose_landmarks.landmark[23].y,11))
                    right_hip.append(Point(results.pose_landmarks.landmark[24].x,results.pose_landmarks.landmark[24].y,12))
                    points = left_shoulder+right_shoulder+left_elbos+right_elbos+left_wirst+right_wrist+left_pinky+right_pinky+left_index+right_index+left_hip+right_hip
                    
                    start = time.time()
                    recognizer = Recognizer(templates)
                    result = recognizer.recognize(points)
                    end = time.time()
                    print(result[0])
                    print("time taken to classify:"+ str(end-start))
                except:
                    pass
            else :
                cap.release()
                break

    cap.release()
    #print(label)
    return points



points = getPoints("test") 
