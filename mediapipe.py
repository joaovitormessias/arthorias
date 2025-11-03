# controle_servos_visual.py - Visualização dos comandos de 18 servos sem hardware

import cv2
import mediapipe as mp
import numpy as np

# ----- MAPEAMENTO DOS SERVOS -----
MAPA_SERVOS = {
    'thumb_prox': 2,
    'thumb_dist': 3,
    'index_prox': 4,
    'index_dist': 5,
    'middle_prox': 6,
    'middle_dist': 7,
    'ring_prox': 8,
    'ring_dist': 9,
    'pinky_prox': 10,
    'pinky_dist': 11,
    'wrist_flex': 12,
    'wrist_lateral': 13,
    'forearm_rotate': 14,  # SERVO DE ROTAÇÃO DO ANTEBRAÇO
    'extra1': 15,
    'extra2': 16,
    'extra3': 17,
    'extra4': 18,
    'extra5': 19
}

# ----- INICIALIZA MEDIAPIPE -----
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(model_complexity=1, max_num_hands=1,
                       min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils
# Captura de vídeo
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
ref_normal = None
prev_angle = 90.0  # ângulo filtrado inicial (neutro)

print("[INFO] Inicializado. Pressione 'q' para sair.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    comandos = {}  # dicionário simulando os comandos enviados aos servos

    if results.multi_hand_world_landmarks:
        hand_landmarks = results.multi_hand_world_landmarks[0]

        mp_drawing.draw_landmarks(
        frame,
        results.multi_hand_landmarks[0],
        mp_hands.HAND_CONNECTIONS,
        mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=3),
        mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2)
        )


        # Pega pontos 3D para vetores de rotação da palma
        p0 = np.array([hand_landmarks.landmark[0].x,
                       hand_landmarks.landmark[0].y,
                       hand_landmarks.landmark[0].z])
        p5 = np.array([hand_landmarks.landmark[5].x,
                       hand_landmarks.landmark[5].y,
                       hand_landmarks.landmark[5].z])
        p17 = np.array([hand_landmarks.landmark[17].x,
                        hand_landmarks.landmark[17].y,
                        hand_landmarks.landmark[17].z])

        v1 = p17 - p0
        v2 = p5 - p17
        normal = np.cross(v1, v2)
        norm = np.linalg.norm(normal)
        normal_unit = normal / norm if norm != 0 else normal

        if ref_normal is None:
            ref_normal = normal_unit

        dot = np.clip(np.dot(ref_normal, normal_unit), -1.0, 1.0)
        theta_rad = np.arccos(dot)
        theta_deg = np.degrees(theta_rad)
        cross_prod = np.cross(ref_normal, normal_unit)
        rotation_sign = np.sign(cross_prod[2])
        angle_signed = rotation_sign * theta_deg
        filtered_angle = 0.8 * prev_angle + 0.2 * (90 + angle_signed)
        prev_angle = filtered_angle
        servo_cmd = int(max(0, min(180, filtered_angle)))
        comandos['forearm_rotate'] = servo_cmd

        # Simula comando para servo dos dedos com base em distancia dos pontos
        def distancia(a, b):
            return np.linalg.norm(np.array([hand_landmarks.landmark[a].x - hand_landmarks.landmark[b].x,
                                            hand_landmarks.landmark[a].y - hand_landmarks.landmark[b].y,
                                            hand_landmarks.landmark[a].z - hand_landmarks.landmark[b].z]))

        dedos = ['thumb', 'index', 'middle', 'ring', 'pinky']
        pares = [(2, 4), (6, 8), (10, 12), (14, 16), (18, 20)]

        for nome, (a, b) in zip(dedos, pares):
            d = distancia(a, b)
            ang = int(np.interp(d, [0.02, 0.08], [160, 20]))  # aproximação = dedo fechado
            comandos[f'{nome}_prox'] = ang
            comandos[f'{nome}_dist'] = ang

    # Mostra feedback visual
    texto = "Comandos (simulados):\n"
    for k, v in comandos.items():
        texto += f"{k}: {v}\u00b0\n"

    frame = cv2.flip(frame, 1)
    y0 = 30
    for i, linha in enumerate(texto.split("\n")):
        cv2.putText(frame, linha, (10, y0 + i*40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (91,255,180), 2)

    cv2.imshow("Visualizacao - Movimento da Mao", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()