# hid_gamepad.py
# Classe mínima para gamepad com:
# - 16 botões declarados
# - POV Hat / D-Pad
# - eixo Z
# - rotação Z

import struct


class Gamepad:
    SOUTH_X = 1
    NORTH_B = 2
    WEST_A = 3
    EAST_Y = 4

    SHARE = 5
    OPTIONS = 6
    HOME = 7
    L1 = 8
    R1 = 9

    HAT_UP = 0
    HAT_UP_RIGHT = 1
    HAT_RIGHT = 2
    HAT_DOWN_RIGHT = 3
    HAT_DOWN = 4
    HAT_DOWN_LEFT = 5
    HAT_LEFT = 6
    HAT_UP_LEFT = 7
    HAT_CENTER = 8

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

        self.send_state(0, self.HAT_CENTER, 0, 0)

    def send_state(self, button_mask, hat, z, rz):
        button_mask = button_mask & 0xFFFF
        hat = hat & 0x0F

        # Report:
        # 2 bytes = botões 1..16
        # 1 byte  = hat nos 4 bits baixos + padding nos 4 bits altos
        # 1 byte  = eixo Z
        # 1 byte  = eixo Rz
        report = struct.pack(
            "<HBbb",
            button_mask,
            hat,
            self._clamp_axis(z),
            self._clamp_axis(rz),
        )

        self._device.send_report(report)

    def _clamp_axis(self, value):
        if value < -127:
            return -127
        if value > 127:
            return 127
        return int(value)