# Simulador de Mão e Antebraço Robótico com Webcam - MediaPipe + OpenCV

import cv2
import mediapipe as mp
import numpy as np

# Inicialização
mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)
joint_angles = np.zeros(18)
prev_angles = joint_angles.copy()
lpf = 0.2  # Suavização

# Define nomes para os 18 servos (dedos e antebraço)
SERVOS = [
    'thumb_prox', 'thumb_dist',
    'index_prox', 'index_dist',
    'middle_prox', 'middle_dist',
    'ring_prox', 'ring_dist',
    'pinky_prox', 'pinky_dist',
    'wrist_flex', 'wrist_lateral', 'forearm_rotate',
    'elbow', 'shoulder_pitch', 'shoulder_yaw', 'shoulder_roll', 'base'
]

def angulo(a, b, c):
    ba = a - b
    bc = c - b
    if np.linalg.norm(ba) == 0 or np.linalg.norm(bc) == 0:
        return 0.0  # ou algum valor neutro, como 90
    cos_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))
    return np.degrees(angle)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = holistic.process(img_rgb)

    frame = cv2.flip(frame, 1)
    h, w = frame.shape[:2]
    texto = "Simulador - Angulos detectados:\n"

    if result.pose_landmarks and result.right_hand_landmarks:
        pose = result.pose_landmarks.landmark
        hand = result.right_hand_landmarks.landmark

        # Ombro, cotovelo, punho (para antebraço)
        shoulder = np.array([pose[mp_holistic.PoseLandmark.RIGHT_SHOULDER].x,
                             pose[mp_holistic.PoseLandmark.RIGHT_SHOULDER].y,
                             pose[mp_holistic.PoseLandmark.RIGHT_SHOULDER].z])
        elbow = np.array([pose[mp_holistic.PoseLandmark.RIGHT_ELBOW].x,
                          pose[mp_holistic.PoseLandmark.RIGHT_ELBOW].y,
                          pose[mp_holistic.PoseLandmark.RIGHT_ELBOW].z])
        wrist = np.array([pose[mp_holistic.PoseLandmark.RIGHT_WRIST].x,
                          pose[mp_holistic.PoseLandmark.RIGHT_WRIST].y,
                          pose[mp_holistic.PoseLandmark.RIGHT_WRIST].z])

        joint_angles[13] = 180 - angulo(shoulder, elbow, wrist)  # Cotovelo
        joint_angles[14] = angulo(elbow, shoulder, wrist)        # Pitch
        joint_angles[15] = angulo(
            np.array([shoulder[0], shoulder[2]]),
            np.array([shoulder[0], shoulder[2]]),
            np.array([elbow[0], elbow[2]])
        )
        joint_angles[16] = 0  # Roll estimado
        joint_angles[17] = 0  # base (caso haja)

        # Dedo médio como exemplo para abrir/fechar
        mcp = np.array([hand[9].x, hand[9].y, hand[9].z])
        pip = np.array([hand[10].x, hand[10].y, hand[10].z])
        dip = np.array([hand[11].x, hand[11].y, hand[11].z])
        tip = np.array([hand[12].x, hand[12].y, hand[12].z])

        joint_angles[4] = angulo(mcp, pip, dip)   # proximal
        joint_angles[5] = angulo(pip, dip, tip)   # distal

        # Torção do antebraço (simplificada com vetor palma)
        palm_vec = np.cross(
            np.array([hand[5].x, hand[5].y, hand[5].z]) - np.array([hand[17].x, hand[17].y, hand[17].z]),
            np.array([hand[9].x, hand[9].y, hand[9].z]) - np.array([hand[0].x, hand[0].y, hand[0].z])
        )
        joint_angles[12] = np.interp(palm_vec[2], [-0.3, 0.3], [0, 180])

        # Aplica filtro LPF
        joint_angles = lpf * joint_angles + (1 - lpf) * prev_angles
        prev_angles = joint_angles.copy()

    # Mostra na tela os valores dos 18 servos simulados
    for i, nome in enumerate(SERVOS):
        val = 0 if np.isnan(joint_angles[i]) else int(joint_angles[i])
        texto += f"{nome}: {val:>3}°\n"

    y0 = 30
    for i, linha in enumerate(texto.split("\n")):
        cv2.putText(frame, linha, (10, y0 + i*20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

    cv2.imshow("Simulador - Membro Superior", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()