import cv2
import mediapipe as mp
import servo as mao  # Arquivo 'servo' importado
import numpy as np

# Configuração inicial da captura de vídeo
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Define a largura do frame
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Define a altura do frame

# Configurações do MediaPipe para detecção de mãos
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

def processa_pontos_mao(img, hand_points):
    """
    Processa os pontos da mão detectada e realiza as ações no servo.
    :param img: Frame de imagem capturado
    :param hand_points: Pontos detectados da mão
    :return: Lista de coordenadas dos pontos da mão
    """
    h, w, _ = img.shape
    pontos = []
    
    # Percorre os pontos da mão detectada
    for points in hand_points:
        mp_draw.draw_landmarks(img, points, mp_hands.HAND_CONNECTIONS)
        
        # Coleta e armazena as coordenadas x e y dos pontos
        for id, cord in enumerate(points.landmark):
            cx, cy = int(cord.x * w), int(cord.y * h)
            cv2.circle(img, (cx, cy), 2, (255, 255, 0), -1)  # Desenha um círculo no ponto
            pontos.append((cx, cy))
    
    return pontos

def calcular_angulo(p1,p2,p3):
    """
    Calcula o ângulo entre três pontos usando a Lei dos Cossenos.
    :param p1: Primeiro ponto (np.array)
    :param p2: Ponto de referência (np.array)
    :param p3: Terceiro ponto (np.array)
    """
    a = np.linalg.norm(p2-p3)
    b = np.linalg.norm(p1-p3)
    c = np.linalg.norm(p1-p2)

    cos_angle = (b**2 + c**2 - a**2)/ (2 * b * c)
    angle = np.arccos(np.clip(cos_angle, -1.0,1.0))

    return np.degrees(angle)

def controlar_servo_com_angulo(pontos):
    """
    Controla o movimento do servo motor com base nos angulos das articulações dos dedos.
    :param pontos: Lista de coordenadas dos pontos da mão
    """
    
    angulo_polegar = calcular_angulo(np.array(pontos[4]),np.array(pontos[0]),np.array(pontos[7]))
    angulo_indicador = calcular_angulo(np.array(pontos[5]), np.array(pontos[6]), np.array(pontos[7]))
    angulo_medio = calcular_angulo(np.array(pontos[9]), np.array(pontos[10]), np.array(pontos[11]))
    angulo_anelar = calcular_angulo(np.array(pontos[13]), np.array(pontos[14]), np.array(pontos[15]))
    angulo_minimo = calcular_angulo(np.array(pontos[17]), np.array(pontos[18]), np.array(pontos[19]))

    mao.abrir_fechar(7,angulo_polegar)
    mao.abrir_fechar(6, angulo_indicador)
    mao.abrir_fechar(5, angulo_medio)
    mao.abrir_fechar(4, angulo_anelar)
    mao.abrir_fechar(3,angulo_minimo)

# Loop principal de captura de vídeo e processamento
while True:
    success, img = cap.read()  # Lê o frame da câmera
    if not success:
        print("Falha ao capturar imagem.")
        break
    
    # Converte a imagem de BGR para RGB
    frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Processa o frame para detectar mãos
    results = hands.process(frame_rgb)
    hand_points = results.multi_hand_landmarks
    
    # Se detectar uma mão, processa os pontos e controla o servo
    if hand_points:
        pontos = processa_pontos_mao(img, hand_points)
        if pontos:
            controlar_servo_com_angulo(pontos)
    
    # Exibe a imagem com os pontos da mão desenhados
    cv2.imshow('Imagem', img)
    
    # Verifica se a tecla 'q' foi pressionada para encerrar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera os recursos ao encerrar
cap.release()
cv2.destroyAllWindows()
