# boot.py
# nice!nano como USB HID Gamepad:
# - 16 botões declarados, 9 usados
# - POV Hat / D-Pad
# - 1 analógico direito usando Eixo Z e Rotação Z

import usb_hid

GAMEPAD_REPORT_DESCRIPTOR = bytes((
    0x05, 0x01,  # Usage Page (Generic Desktop Controls)
    0x09, 0x05,  # Usage (Game Pad)
    0xA1, 0x01,  # Collection (Application)

    0x85, 0x01,  # Report ID (1)

    # ------------------------------------------------------------
    # 16 botões
    # ------------------------------------------------------------
    0x05, 0x09,  # Usage Page (Button)
    0x19, 0x01,  # Usage Minimum (Button 1)
    0x29, 0x10,  # Usage Maximum (Button 16)
    0x15, 0x00,  # Logical Minimum (0)
    0x25, 0x01,  # Logical Maximum (1)
    0x75, 0x01,  # Report Size (1 bit)
    0x95, 0x10,  # Report Count (16)
    0x81, 0x02,  # Input (Data, Variable, Absolute)

    # ------------------------------------------------------------
    # POV Hat / D-Pad
    # 0 = cima
    # 1 = cima + direita
    # 2 = direita
    # 3 = baixo + direita
    # 4 = baixo
    # 5 = baixo + esquerda
    # 6 = esquerda
    # 7 = cima + esquerda
    # 8 = neutro
    # ------------------------------------------------------------
    0x05, 0x01,  # Usage Page (Generic Desktop Controls)
    0x09, 0x39,  # Usage (Hat Switch)
    0x15, 0x00,  # Logical Minimum (0)
    0x25, 0x07,  # Logical Maximum (7)
    0x35, 0x00,  # Physical Minimum (0)
    0x46, 0x3B, 0x01,  # Physical Maximum (315)
    0x65, 0x14,  # Unit (English Rotation, degrees)
    0x75, 0x04,  # Report Size (4 bits)
    0x95, 0x01,  # Report Count (1)
    0x81, 0x42,  # Input (Data, Variable, Absolute, Null State)
    0x65, 0x00,  # Unit (None)

    # 4 bits de padding para fechar byte
    0x75, 0x04,  # Report Size (4 bits)
    0x95, 0x01,  # Report Count (1)
    0x81, 0x03,  # Input (Constant, Variable, Absolute)

    # ------------------------------------------------------------
    # Analógico direito:
    # Z  = eixo Z
    # Rz = rotação Z
    # ------------------------------------------------------------
    0x05, 0x01,  # Usage Page (Generic Desktop Controls)
    0x09, 0x32,  # Usage (Z)
    0x09, 0x35,  # Usage (Rz)

    0x15, 0x81,  # Logical Minimum (-127)
    0x25, 0x7F,  # Logical Maximum (127)
    0x75, 0x08,  # Report Size (8 bits)
    0x95, 0x02,  # Report Count (2)
    0x81, 0x02,  # Input (Data, Variable, Absolute)

    0xC0,        # End Collection
))

gamepad = usb_hid.Device(
    report_descriptor=GAMEPAD_REPORT_DESCRIPTOR,
    usage_page=0x01,
    usage=0x05,
    report_ids=(1,),
    in_report_lengths=(5,),   # 2 bytes botões + 1 byte hat/padding + Z + Rz
    out_report_lengths=(0,),
)

try:
    usb_hid.set_interface_name("DACC Station Joystick")
except AttributeError:
    pass

usb_hid.enable((gamepad,))