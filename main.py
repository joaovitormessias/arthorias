import cv2
import mediapipe as mp
import servo as mao  # Arquivo 'servo' importado

# Configuração inicial da captura de vídeo
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Define a largura do frame
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Define a altura do frame

# Configurações do MediaPipe para detecção de mãos
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

def process_hand_points(img, hand_points):
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
            cv2.circle(img, (cx, cy), 4, (255, 0, 0), -1)  # Desenha um círculo no ponto
            pontos.append((cx, cy))
    
    return pontos

def controlar_servo(pontos):
    """
    Controla o movimento do servo motor com base nas distâncias entre os dedos.
    :param pontos: Lista de coordenadas dos pontos da mão
    """
    # Calcula as distâncias entre os dedos para definir os movimentos
    dist_polegar = abs(pontos[17][0] - pontos[4][0])
    dist_indicador = pontos[5][1] - pontos[8][1]
    dist_medio = pontos[9][1] - pontos[12][1]
    dist_anelar = pontos[13][1] - pontos[16][1]
    dist_minimo = pontos[17][1] - pontos[20][1]
    
    # Controla o servo com base nas distâncias dos dedos
    mao.abrir_fechar(7, 0 if dist_polegar < 80 else 1)
    mao.abrir_fechar(6, 1 if dist_indicador >= 1 else 0)
    mao.abrir_fechar(5, 1 if dist_medio >= 1 else 0)
    mao.abrir_fechar(4, 1 if dist_anelar >= 1 else 0)
    mao.abrir_fechar(3, 1 if dist_minimo >= 1 else 0)

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
        pontos = process_hand_points(img, hand_points)
        if pontos:
            controlar_servo(pontos)
    
    # Exibe a imagem com os pontos da mão desenhados
    cv2.imshow('Imagem', img)
    
    # Verifica se a tecla 'q' foi pressionada para encerrar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera os recursos ao encerrar
cap.release()
cv2.destroyAllWindows()
