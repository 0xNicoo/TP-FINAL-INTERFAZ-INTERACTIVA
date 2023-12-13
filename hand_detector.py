import cv2
import mediapipe as mp
import numpy as np

class HandDetector():
    def __init__(self) -> None:
        self.mp_hands = mp.solutions.hands
        self.mp_hands_detection = self.mp_hands.Hands()
        self.central_x=0
        self.central_y=0
        self.hand_close = False
        self.hand_drawing = False
        self.THRESHOLD = 0.08

    def findHands(self, img) -> tuple[int, int]:
        hand_detection = self.mp_hands_detection.process(img)
        if hand_detection.multi_hand_landmarks:
            for hands in hand_detection.multi_hand_landmarks:
                #Calcular el centro
                self.central_x = int(hands.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].x * img.shape[1])
                self.central_y = int(hands.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y * img.shape[0])

                #MANO CERRADA
                thumb_tip = hands.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
                index_finger_tip = hands.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                #Calcula la distancia entre la punta del dedo indice y la punta el dedo pulgar
                distance = cv2.norm(np.array([thumb_tip.x, thumb_tip.y]) - np.array([index_finger_tip.x, index_finger_tip.y]))
                self.hand_close = True if distance < self.THRESHOLD else False

                #MANO DIBUJANDO (indice levantado)
                pinky_tip = hands.landmark[self.mp_hands.HandLandmark.PINKY_TIP]
                #Calcula la distancia entre la punta del dedo meñique y la punta el dedo pulgar
                distance = cv2.norm(np.array([thumb_tip.x, thumb_tip.y]) - np.array([pinky_tip.x, pinky_tip.y]))
                self.hand_drawing = True if distance < self.THRESHOLD else False
        return self.central_x, self.central_y