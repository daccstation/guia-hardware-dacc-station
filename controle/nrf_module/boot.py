# boot.py
# nice!nano como USB HID Gamepad para o DACC Station:
# - 17 posições lógicas de botão (13 entradas físicas utilizadas)
# - D-Pad enviado como botões independentes b12..b15
# - 4 eixos HID (X, Y, Z, Rx)
# - joystick físico enviado em Z/Rx; X/Y permanecem centralizados

import usb_hid


GAMEPAD_REPORT_DESCRIPTOR = bytes((
    0x05, 0x01,        # Usage Page (Generic Desktop Controls)
    0x09, 0x05,        # Usage (Game Pad)
    0xA1, 0x01,        # Collection (Application)

    0x85, 0x01,        # Report ID (1)

    # ------------------------------------------------------------
    # 17 botões lógicos (Button 1..17)
    # ------------------------------------------------------------
    0x05, 0x09,        # Usage Page (Button)
    0x19, 0x01,        # Usage Minimum (Button 1)
    0x29, 0x11,        # Usage Maximum (Button 17)
    0x15, 0x00,        # Logical Minimum (0)
    0x25, 0x01,        # Logical Maximum (1)
    0x75, 0x01,        # Report Size (1 bit)
    0x95, 0x11,        # Report Count (17)
    0x81, 0x02,        # Input (Data, Variable, Absolute)

    # 7 bits de padding para fechar 3 bytes de botões
    0x75, 0x07,        # Report Size (7 bits)
    0x95, 0x01,        # Report Count (1)
    0x81, 0x03,        # Input (Constant, Variable, Absolute)

    # ------------------------------------------------------------
    # 4 eixos assinados de 8 bits
    # X, Y ficam disponíveis para compatibilidade.
    # O joystick físico atual é enviado em Z e Rx.
    # ------------------------------------------------------------
    0x05, 0x01,        # Usage Page (Generic Desktop Controls)
    0x09, 0x30,        # Usage (X)
    0x09, 0x31,        # Usage (Y)
    0x09, 0x32,        # Usage (Z)
    0x09, 0x33,        # Usage (Rx)
    0x15, 0x81,        # Logical Minimum (-127)
    0x25, 0x7F,        # Logical Maximum (127)
    0x75, 0x08,        # Report Size (8 bits)
    0x95, 0x04,        # Report Count (4)
    0x81, 0x02,        # Input (Data, Variable, Absolute)

    0xC0,              # End Collection
))


gamepad = usb_hid.Device(
    report_descriptor=GAMEPAD_REPORT_DESCRIPTOR,
    usage_page=0x01,
    usage=0x05,
    report_ids=(1,),
    in_report_lengths=(7,),  # 3 bytes botões + X + Y + Z + Rx
    out_report_lengths=(0,),
)

try:
    usb_hid.set_interface_name("DACC Station Joystick")
except AttributeError:
    pass

usb_hid.enable((gamepad,))
