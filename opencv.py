import numpy as np
import cv2 as cv

# Localiza a camera
cap = cv.VideoCapture(0)

# Verifica se a camera esta disponivel
if not cap.isOpened():
    print("Falha ao abrir camera, certifique-se que \n - esse canal nao esta sendo utilizado \n - o cabo esta devidamente conectado")
    exit()

# Loop de captura e leitura dos frames
while True:
    '''
    Devolve dois parametros:
    param: ret <- True | False
    param: frame: <- imagem capturada
    '''
    ret, frame  = cap.read() # Le os frames da camera em tempo de captura

    # Se nao houver captura de frame ou seja ret = False encerra captura
    if not ret:
        print("Houve falha na captura do frame! \n Utilize um ambiente bem iluminado para que os frames consigam ser capturados")
        break

    # Manipulacao dos frames vem aqui
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) # bgr to color that i want to display
    # Exibe o frame seguindo a escolha da cor processada
    cv.imshow('frame', gray)
    # Tecla para eu poder finalizar a captura
    if cv.waitKey(1) == ord('q'):
        break

# Libera a camera
cap.release()
cv.destroyAllWindows()
