import os
import cv2
import numpy as np
import mediapipe as mp
from pyfirmata import Arduino, util, SERVO
import time

# Conexão com Arduino Nano RP2040 com ConfigurableFirmata
board = Arduino('COM3')

# Pinos físicos usados nos servos (exemplo)
servo_pinos = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

# Inicializa os pinos como servos
for p in servo_pinos:
    board.digital[p].mode = SERVO
    board.digital[p].write(90)  # posição neutra inicial
    time.sleep(0.02)

# Mapeia os nomes dos servos para seus respectivos pinos
servo_map = {
    'thumb_prox': 2, 'thumb_dist': 3, 'thumb_lat': 4,
    'index_prox': 5, 'index_dist': 6, 'index_lat': 7,
    'middle_prox': 8, 'middle_dist': 9, 'middle_lat': 10,
    'ring_prox': 11, 'ring_dist': 12, 'ring_lat': 13,
    'pinky_prox': 14, 'pinky_dist': 15, 'pinky_lat': 16,
    'wrist_flex': 17, 'wrist_lateral': 18, 'forearm_rotate': 19
}

# Inicializa MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(model_complexity=1, max_num_hands=1,
                       min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Funções matemáticas

def normalizar(vetor):
    norma = np.linalg.norm(vetor)
    return vetor / norma if norma != 0 else vetor

def calcular_angulo(v1, v2):
    v1_u = normalizar(v1)
    v2_u = normalizar(v2)
    dot = np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)
    return np.degrees(np.arccos(dot))

def produto_vetorial(v1, v2):
    return np.cross(v1, v2)

def suavizar_angulo(prev, atual, fator=0.2):
    return (1 - fator) * prev + fator * atual

def distancia(lm, a, b):
    return np.linalg.norm(np.array([
        lm[a].x - lm[b].x,
        lm[a].y - lm[b].y,
        lm[a].z - lm[b].z
    ]))

# Inicializa captura de vídeo
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

ref_normal = None
prev_angle = 90.0

print("[INFO] Controle ativo. Pressione 'q' para sair.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    comandos = {}

    if results.multi_hand_world_landmarks and results.multi_handedness:
        hand_label = results.multi_handedness[0].classification[0].label
        if hand_label == "Left":
            lm = results.multi_hand_world_landmarks[0].landmark

            mp_drawing.draw_landmarks(
                frame,
                results.multi_hand_landmarks[0],
                mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=4),
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2)
            )

            # ROTAÇÃO DO ANTEBRAÇO
            p0 = np.array([lm[0].x, lm[0].y, lm[0].z])
            p5 = np.array([lm[5].x, lm[5].y, lm[5].z])
            p17 = np.array([lm[17].x, lm[17].y, lm[17].z])
            v1 = p17 - p0
            v2 = p5 - p17
            normal = produto_vetorial(v1, v2)
            normal_unit = normalizar(normal)

            if ref_normal is None:
                ref_normal = normal_unit

            theta_deg = calcular_angulo(ref_normal, normal_unit)
            rotation_sign = np.sign(produto_vetorial(ref_normal, normal_unit)[2])
            angle_signed = rotation_sign * theta_deg
            filtered_angle = suavizar_angulo(prev_angle, 90 + angle_signed)
            prev_angle = filtered_angle
            servo_cmd = int(np.clip(filtered_angle, 0, 180))
            comandos['forearm_rotate'] = servo_cmd

            # DEDOS
            dedos = ['thumb', 'index', 'middle', 'ring', 'pinky']
            pares = [(2, 4), (6, 8), (10, 12), (14, 16), (18, 20)]
            laterais = [(1, 2), (5, 6), (9, 10), (13, 14), (17, 18)]

            for nome, (a, b), (la, lb) in zip(dedos, pares, laterais):
                d = distancia(lm, a, b)
                ang = int(np.interp(d, [0.02, 0.08], [160, 20]))
                comandos[f'{nome}_prox'] = ang
                comandos[f'{nome}_dist'] = ang

                dlat = distancia(lm, la, lb)
                lang = int(np.interp(dlat, [0.01, 0.05], [180, 0]))
                comandos[f'{nome}_lat'] = lang

    # ENVIA PARA OS SERVOS CONECTADOS
    for nome, valor in comandos.items():
        if nome in servo_map:
            pino = servo_map[nome]
            board.digital[pino].write(valor)

    # MOSTRA A INTERFACE VISUAL
    texto = "Comandos (atuais):\n"
    for nome in servo_map:
        if nome in comandos:
            texto += f"{nome}: {comandos[nome]}°\n"

    frame = cv2.flip(frame, 1)
    y0 = 30
    for i, linha in enumerate(texto.split("\n")):
        cv2.putText(frame, linha, (10, y0 + i*26), cv2.FONT_HERSHEY_DUPLEX, 0.8, (91,255,180), 2)

    cv2.imshow("Controle Braco Robo - MediaPipe", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
board.exit()
