from pyfirmata import Arduino, SERVO
import time

# configuracao da placa Arduino
board = Arduino('COM5')

# definicao dos pinos para controle dos servos
servo_pins = {
    'polegar': 7,
    'indicador': 6,
    'medio': 5,
    'anelar': 4,
    'minimo': 3
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

def abrir_fechar(pin, on_off):
    """
    abre ou fecha um servo motor com base no estado de controle
    :param pin: pino ao qual o servo está conectado
    :param on_off: 1 para abrir, 0 para fechar
    """
    if on_off == 1:
        rotate_servo(pin, 0)  # abre o servo (posicao 0 graus)
    else:
        if pin == servo_pins['polegar']:
            rotate_servo(pin, 100)  # posicao de fechamento específica para o polegar
        elif pin == servo_pins['indicador']:
            rotate_servo(pin, 120)  # posicao de fechamento específica para o indicador
        else:
            rotate_servo(pin, 120)  # posicao de fechamento padrão para outros dedos

def testar_todos():
    """
    testa o movimento de todos os servos, abrindo e fechando os dedos em sequencia
    """
    # abrir todos os dedos
    for pin in servo_pins.values():
        rotate_servo(pin, 0)
    time.sleep(1)

    # fechar todos os dedos um por um, com delays entre cada um
    for dedo, pin in servo_pins.items():
        if dedo == 'polegar':
            rotate_servo(pin, 120)
        elif dedo == 'indicador':
            rotate_servo(pin, 100)
        else:
            rotate_servo(pin, 100)
        time.sleep(1)
        rotate_servo(pin, 0)
        time.sleep(1)

    time.sleep(2)

# exemplo de uso
if __name__ == '__main__':
    testar_todos()
