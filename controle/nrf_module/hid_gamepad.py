# hid_gamepad.py
# Relatório HID do DACC Station:
# - 17 posições lógicas de botão (b0..b16)
# - 4 eixos: X, Y, Z e Rx

import struct


class Gamepad:
    # Índices lógicos HID / índices observados como b0..b16.
    # Alguns índices ficam intencionalmente sem entrada física para manter
    # o layout usado pela camada de compatibilidade Linux.
    A = 0
    B = 1
    Y = 2
    X = 3

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

        self.send_state(0, 0, 0, 0, 0)

    def send_state(self, button_mask, x, y, z, rx):
        button_mask &= 0x1FFFF

        # 17 bits de botões ocupam 3 bytes; os 7 bits altos do terceiro
        # byte permanecem em zero. Depois seguem X, Y, Z e Rx como int8.
        report = bytes((
            button_mask & 0xFF,
            (button_mask >> 8) & 0xFF,
            (button_mask >> 16) & 0x01,
        )) + struct.pack(
            "<bbbb",
            self._clamp_axis(x),
            self._clamp_axis(y),
            self._clamp_axis(z),
            self._clamp_axis(rx),
        )

        self._device.send_report(report)

    @staticmethod
    def _clamp_axis(value):
        if value < -127:
            return -127
        if value > 127:
            return 127
        return int(value)
