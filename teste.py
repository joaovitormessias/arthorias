from pyfirmata import Arduino, SERVO
import time

# inicializacao da placa Arduino
board = Arduino('COM10')

# mapeamento dos pinos para os dedos do braço robótico
servo_pins = {
    'polegar': 7,
    'indicador': 6,
    'medio': 5,
    'anelar': 4,
    'minimo': 3
}

# config dos pinos no modo SERVO
for pin in servo_pins.values():
    board.digital[pin].mode = SERVO

def rotate_servo(pin, angle):
    """
    gira o servo motor para o angulo especificado
    :param pin: Pino do servo motor
    :param angle: angulo para o qual o servo deve girar (0 a 180 graus)
    """
    board.digital[pin].write(angle)
    time.sleep(0.015)  # pequena pausa para garantir que o servo complete o movimento

def testar_todos(tempo_espera=1):
    """
    testa todos os servos motores movendo-os entre as posições de abertura e fechamento
    :param tempo_espera: tempo de espera entre cada movimento em segundos
    """
    # abrir todos os dedos
    for pin in servo_pins.values():
        rotate_servo(pin, 0)  # Posição de abertura total
    time.sleep(tempo_espera)

    # fechar e abrir cada dedo individualmente
    for dedo, pin in servo_pins.items():
        fechar_angulo = 130 if dedo == 'polegar' else 110  # angulo de fechamento diferente para o polegar
        rotate_servo(pin, fechar_angulo)  # fechar o dedo
        time.sleep(tempo_espera)
        rotate_servo(pin, 0)  # abrir o dedo novamente
        time.sleep(tempo_espera)

if __name__ == '__main__':
    testar_todos()

