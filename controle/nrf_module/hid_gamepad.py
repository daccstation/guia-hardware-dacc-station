# hid_gamepad.py
# Classe minima para gamepad com:
# - 17 botoes declarados
# - D-Pad como botoes independentes
# - 4 eixos HID: X, Y, Z, Rx
# - X/Y centralizados; analogico fisico em Z/Rx

import struct


class Gamepad:
    # Indices SDL / Godot esperados (b0, b1, ...)
    SOUTH_X = 0
    NORTH_B = 1
    WEST_A = 2
    EAST_Y = 3

    L1 = 4
    R1 = 5

    SHARE = 8
    OPTIONS = 9

    DPAD_UP = 12
    DPAD_DOWN = 13
    DPAD_LEFT = 14
    DPAD_RIGHT = 15

    HOME = 16

    def __init__(self, devices):
        self._device = None

        for device in devices:
            if device.usage_page == 0x01 and device.usage == 0x05:
                self._device = device
                break

        if self._device is None:
            raise RuntimeError(
                "Gamepad HID nao encontrado. Verifique o boot.py e reinicie a placa."
            )

        self.send_state(0, 0, 0)

    def send_state(self, button_mask, right_x, right_y):
        # 17 bits de botoes => 3 bytes.
        button_mask = button_mask & 0x1FFFF

        buttons = bytes((
            button_mask & 0xFF,
            (button_mask >> 8) & 0xFF,
            (button_mask >> 16) & 0x01,
        ))

        # O host recebe quatro eixos nos usages X, Y, Z, Rx.
        # No Windows/Chromium isso ocupa os indices 0, 1, 2 e 3.
        # Left X/Left Y ficam no centro e o analogico fisico controla
        # axis 2 (Right X) e axis 3 (Right Y).
        axes = struct.pack(
            "bbbb",
            0,
            0,
            self._clamp_axis(right_x),
            self._clamp_axis(right_y),
        )

        self._device.send_report(buttons + axes)

    def _clamp_axis(self, value):
        if value < -127:
            return -127
        if value > 127:
            return 127
        return int(value)
