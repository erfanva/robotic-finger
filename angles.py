### Imports
import mediapipe as mp
import cv2
import numpy as np
import serial

###
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)
###
temp = [180, 180, 180]
###
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

###
joint_list = [[8,7,6], [12,11,10], [16,15,14], [20,19,18]]

###
def find_finger_angles(image, results, joint_list):
    
    # Loop through hands
    res_angles = []
    for hand in results.multi_hand_landmarks:
        one_hand_angles = []
        #Loop through joint sets 
        for joint in joint_list:
            a = np.array([hand.landmark[joint[0]].x, hand.landmark[joint[0]].y]) # First coord
            b = np.array([hand.landmark[joint[1]].x, hand.landmark[joint[1]].y]) # Second coord
            c = np.array([hand.landmark[joint[2]].x, hand.landmark[joint[2]].y]) # Third coord
            
            radians = np.arctan2(c[1] - b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
            angle = np.abs(radians*180.0/np.pi)
            
            if angle > 180.0:
                angle = 360-angle
            
            one_hand_angles.append(angle)
            
            cv2.putText(image, str(round(angle, 2)), tuple(np.multiply(b, [640, 480]).astype(int)),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        res_angles.append(one_hand_angles)
    return res_angles


###
cap = cv2.VideoCapture(1)

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands: 
    while cap.isOpened():
        ret, frame = cap.read()
        
        # BGR 2 RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Flip on horizontal
        image = cv2.flip(image, 1)
        
        # Set flag
        image.flags.writeable = False
        
        # Detections
        results = hands.process(image)
        
        # Set flag to true
        image.flags.writeable = True
        
        # RGB 2 BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Detections
        #print(results)
        
        # Rendering results
        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS, 
                                        mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                        mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                                         )
                
            
            # Find and Draw angles to image from joint list
            angles = find_finger_angles(image, results, joint_list)

            first_hand_angles = angles[0]
            index_finger_angle = first_hand_angles[0]
            del temp[0]
            temp.append(index_finger_angle)
            #### command to robot
            # print('first')
            # print(index_finger_angle)
            if temp[0] <= 140 and temp[1] <= 140 and temp[2] <= 140:
                arduino.write(bytes('0', 'utf-8'))
            elif temp[0] > 140 and temp[1] > 140 and temp[2] > 140:
                arduino.write(bytes('1', 'utf-8'))
            
        # Save our image    
        #cv2.imwrite(os.path.join('Output Images', '{}.jpg'.format(uuid.uuid1())), image)
        cv2.imshow('Hand Tracking', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
