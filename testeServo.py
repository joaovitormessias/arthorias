from pyfirmata import Arduino, SERVO
import time

# configuracao da placa Arduino
board = Arduino('COM10')

# definicao dos pinos para controle dos servos
servo_pins = {
    'polegar': 7,
    'indicador': 6,
    'medio': 5,
    'anelar': 4,
    'minimo': 3,
    'ombro': 12,
    'cotovelo': 13,
}

# configuracao dos pinos no modo SERVO
for pin in servo_pins.values():
    board.digital[pin].mode = SERVO

def rotate_servo(pin, angle):
    """
    gira o servo motor para um angulo específico
    :param pin: pino ao qual o servo está conectado
    :param angle: angulo para o qual o servo deve girar (0 a 180 graus)
    """
    board.digital[pin].write(angle)
    time.sleep(0.015)  # delay necessário para dar tempo ao servo para mover

def abrir_fechar(pin, angle):
    """
    abre ou fecha um servo motor com base no estado de controle
    :param pin: pino ao qual o servo está conectado
    :param angle: ângulo calculado para a posição do servo (0 a 180 graus)
    """

    angle = max(0, min(180,angle)) # garante que o ângulo não ultrapasse os limites
    rotate_servo(pin,angle) # gira o servo para o ângulo calculado