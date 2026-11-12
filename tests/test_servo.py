"""No serial port or physical servo is touched by these tests."""
import importlib.util
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import MagicMock, patch

class ServoTests(unittest.TestCase):
    def test_port_configuration_and_open_close_angles(self):
        firmata = MagicMock()
        spec = importlib.util.spec_from_file_location("tested_servo", Path(__file__).parents[1] / "servo.py")
        module = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, {"pyfirmata": firmata}), patch.dict(os.environ, {"ARDUINO_PORT": "/dev/test"}), patch("time.sleep"):
            spec.loader.exec_module(module)
            firmata.Arduino.assert_called_once_with("/dev/test")
            for pin, closed in [(7,100),(6,120),(5,120),(4,120),(3,120)]:
                module.abrir_fechar(pin, 0)
                module.board.digital[pin].write.assert_called_with(closed)
                module.abrir_fechar(pin, 1)
                module.board.digital[pin].write.assert_called_with(0)
