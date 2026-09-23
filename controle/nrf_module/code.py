# code.py
# Controle USB HID do DACC Station para nice!nano:
# - 13 botões físicos em 17 posições HID
# - D-Pad como botões independentes b12..b15
# - 1 joystick analógico enviado como Z/Rx (analógico direito)
# - X/Y HID mantidos centralizados
# - calibração automática, deadzone e suavização

import time
import board
import digitalio
import analogio
import usb_hid

from hid_gamepad import Gamepad


# -------------------------------------------------------------------
# PINOS DOS BOTÕES PRINCIPAIS
# -------------------------------------------------------------------

# Mapeamento físico validado com a camada Linux:
# b0=A, b1=B, b2=Y, b3=X
PIN_A = board.P1_11
PIN_B = board.P0_10
PIN_Y = board.P0_09
PIN_X = board.P1_13


# -------------------------------------------------------------------
# PINOS DO D-PAD
# -------------------------------------------------------------------

PIN_DPAD_UP = board.P1_00
PIN_DPAD_DOWN = board.P0_11
PIN_DPAD_LEFT = board.P1_04
PIN_DPAD_RIGHT = board.P1_06


# -------------------------------------------------------------------
# PINOS DOS BOTÕES EXTRAS
# -------------------------------------------------------------------

PIN_SHARE = board.P0_06
PIN_OPTIONS = board.P0_08
PIN_HOME = board.P0_17
PIN_L1 = board.P0_20
PIN_R1 = board.P0_22


# -------------------------------------------------------------------
# PINOS DO ANALÓGICO
# -------------------------------------------------------------------

PIN_AXIS_X = board.AIN0  # P0_02
PIN_AXIS_Y = board.AIN5  # P0_29


# -------------------------------------------------------------------
# AJUSTES DO ANALÓGICO
# -------------------------------------------------------------------

DEADZONE = 42
SMOOTHING = 0.60

INVERT_X = False
INVERT_Y = True

LOOP_DELAY = 0.01
PRINT_INTERVAL = 0.2

# Limites observados no protótipo.
AXIS_X_MIN = 0
AXIS_X_MAX = 51200
AXIS_Y_MIN = 0
AXIS_Y_MAX = 51200


def setup_button(pin):
    button = digitalio.DigitalInOut(pin)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP
    return button


def calibrate_axis(axis, samples=100):
    total = 0

    for _ in range(samples):
        total += axis.value
        time.sleep(0.005)

    return total // samples


def apply_smoothing(previous, current):
    return previous + (current - previous) * SMOOTHING


def clamp(value, minimum, maximum):
    if value < minimum:
        return minimum
    if value > maximum:
        return maximum
    return value


def convert_axis(value, center, raw_min, raw_max, invert=False):
    if value >= center:
        denominator = raw_max - center
        if denominator <= 0:
            axis = 0
        else:
            axis = int(((value - center) * 127) / denominator)
    else:
        denominator = center - raw_min
        if denominator <= 0:
            axis = 0
        else:
            axis = -int(((center - value) * 127) / denominator)

    axis = clamp(axis, -127, 127)

    if -DEADZONE < axis < DEADZONE:
        axis = 0

    if invert:
        axis = -axis

    return clamp(axis, -127, 127)


def set_button(mask, index):
    return mask | (1 << index)


# -------------------------------------------------------------------
# SETUP
# -------------------------------------------------------------------

button_a = setup_button(PIN_A)
button_b = setup_button(PIN_B)
button_y = setup_button(PIN_Y)
button_x = setup_button(PIN_X)

l1 = setup_button(PIN_L1)
r1 = setup_button(PIN_R1)
share = setup_button(PIN_SHARE)
options = setup_button(PIN_OPTIONS)
home = setup_button(PIN_HOME)

dpad_up = setup_button(PIN_DPAD_UP)
dpad_down = setup_button(PIN_DPAD_DOWN)
dpad_left = setup_button(PIN_DPAD_LEFT)
dpad_right = setup_button(PIN_DPAD_RIGHT)

axis_x = analogio.AnalogIn(PIN_AXIS_X)
axis_y = analogio.AnalogIn(PIN_AXIS_Y)

gamepad = Gamepad(usb_hid.devices)

print("nice!nano USB HID Gamepad iniciado.")
print("Mantenha o analogico parado no centro para calibrar...")

time.sleep(1)

center_x = calibrate_axis(axis_x)
center_y = calibrate_axis(axis_y)

filtered_x = center_x
filtered_y = center_y

print("Calibracao concluida.")
print("Centro X:", center_x)
print("Centro Y:", center_y)
print()
print("Mapeamento HID:")
print("b0  = A")
print("b1  = B")
print("b2  = Y")
print("b3  = X")
print("b4  = L1")
print("b5  = R1")
print("b8  = SHARE/BACK")
print("b9  = OPTIONS/START")
print("b12 = DPAD UP")
print("b13 = DPAD DOWN")
print("b14 = DPAD LEFT")
print("b15 = DPAD RIGHT")
print("b16 = HOME/GUIDE")
print("Z/Rx = joystick direito")
print()

last_buttons = None
last_x = None
last_y = None
last_print_time = 0


# -------------------------------------------------------------------
# LOOP PRINCIPAL
# -------------------------------------------------------------------

while True:
    button_mask = 0

    if not button_a.value:
        button_mask = set_button(button_mask, Gamepad.A)
    if not button_b.value:
        button_mask = set_button(button_mask, Gamepad.B)
    if not button_y.value:
        button_mask = set_button(button_mask, Gamepad.Y)
    if not button_x.value:
        button_mask = set_button(button_mask, Gamepad.X)

    if not l1.value:
        button_mask = set_button(button_mask, Gamepad.L1)
    if not r1.value:
        button_mask = set_button(button_mask, Gamepad.R1)

    if not share.value:
        button_mask = set_button(button_mask, Gamepad.SHARE)
    if not options.value:
        button_mask = set_button(button_mask, Gamepad.OPTIONS)

    if not dpad_up.value:
        button_mask = set_button(button_mask, Gamepad.DPAD_UP)
    if not dpad_down.value:
        button_mask = set_button(button_mask, Gamepad.DPAD_DOWN)
    if not dpad_left.value:
        button_mask = set_button(button_mask, Gamepad.DPAD_LEFT)
    if not dpad_right.value:
        button_mask = set_button(button_mask, Gamepad.DPAD_RIGHT)

    if not home.value:
        button_mask = set_button(button_mask, Gamepad.HOME)

    raw_x = axis_x.value
    raw_y = axis_y.value

    filtered_x = apply_smoothing(filtered_x, raw_x)
    filtered_y = apply_smoothing(filtered_y, raw_y)

    x = convert_axis(
        filtered_x,
        center_x,
        AXIS_X_MIN,
        AXIS_X_MAX,
        invert=INVERT_X,
    )

    y = convert_axis(
        filtered_y,
        center_y,
        AXIS_Y_MIN,
        AXIS_Y_MAX,
        invert=INVERT_Y,
    )

    if button_mask != last_buttons or x != last_x or y != last_y:
        # O descritor expõe quatro eixos. X/Y permanecem centralizados e o
        # joystick físico é enviado em Z/Rx, que a camada Linux converte
        # para ABS_RX/ABS_RY no controle virtual.
        gamepad.send_state(button_mask, 0, 0, x, y)

        last_buttons = button_mask
        last_x = x
        last_y = y

    now = time.monotonic()

    if now - last_print_time >= PRINT_INTERVAL:
        last_print_time = now
        print(
            "RAW_X:", raw_x,
            "RAW_Y:", raw_y,
            "| FILT_X:", int(filtered_x),
            "FILT_Y:", int(filtered_y),
            "| HID_Z:", x,
            "HID_RX:", y,
            "| Buttons:", bin(button_mask),
        )

    time.sleep(LOOP_DELAY)
