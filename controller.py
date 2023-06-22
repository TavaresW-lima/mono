from serial import Serial
from typing import Tuple

RIGHT = 1
LEFT = 0
UP = 1
DOWN = 0


class Controller:
    def __init__(self, device: Serial):
        self.device = device

        print("Comunicação com Arduino iniciada")

    def move(self, values: Tuple[int, int, int, int]):
        senX, velX, senY, velY = values
        command = f"<{senX},{velX},{senY},{velY}>"
        self.device.write(command.encode("utf-8"))
