# code.py
# Controle USB HID básico para nice!nano:
# - 9 botões
# - POV Hat / D-Pad
# - 1 analógico direito com Z/Rz
# - centro automático
# - limites reais manuais
# - deadzone
# - suavização
# - print dos valores dos eixos

import time
import board
import digitalio
import analogio
import usb_hid

from hid_gamepad import Gamepad


# -------------------------------------------------------------------
# PINOS DOS BOTÕES PRINCIPAIS
# -------------------------------------------------------------------

PIN_SOUTH_X = board.P0_09
PIN_NORTH_B = board.P0_10
PIN_WEST_A = board.P1_11
PIN_EAST_Y = board.P1_13


# -------------------------------------------------------------------
# PINOS DAS SETAS / POV HAT
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
PIN_R1 = board.P0_22 #


# -------------------------------------------------------------------
# PINOS DO ANALÓGICO
# -------------------------------------------------------------------

PIN_AXIS_X = board.AIN0  # P0_02 / 002
PIN_AXIS_Y = board.AIN5  # P0_29 / 029


# -------------------------------------------------------------------
# AJUSTES DO ANALÓGICO
# -------------------------------------------------------------------

DEADZONE = 42
SMOOTHING = 0.60

INVERT_X = False
INVERT_Y = True

LOOP_DELAY = 0.01
PRINT_INTERVAL = 0.2


# -------------------------------------------------------------------
# LIMITES REAIS DO ANALÓGICO
# -------------------------------------------------------------------

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


def read_hat(up_pressed, down_pressed, left_pressed, right_pressed):
    if up_pressed and right_pressed:
        return Gamepad.HAT_UP_RIGHT

    if right_pressed and down_pressed:
        return Gamepad.HAT_DOWN_RIGHT

    if down_pressed and left_pressed:
        return Gamepad.HAT_DOWN_LEFT

    if left_pressed and up_pressed:
        return Gamepad.HAT_UP_LEFT

    if up_pressed:
        return Gamepad.HAT_UP

    if right_pressed:
        return Gamepad.HAT_RIGHT

    if down_pressed:
        return Gamepad.HAT_DOWN

    if left_pressed:
        return Gamepad.HAT_LEFT

    return Gamepad.HAT_CENTER


# -------------------------------------------------------------------
# SETUP
# -------------------------------------------------------------------

south_x = setup_button(PIN_SOUTH_X)
north_b = setup_button(PIN_NORTH_B)
west_a = setup_button(PIN_WEST_A)
east_y = setup_button(PIN_EAST_Y)

dpad_up = setup_button(PIN_DPAD_UP)
dpad_down = setup_button(PIN_DPAD_DOWN)
dpad_left = setup_button(PIN_DPAD_LEFT)
dpad_right = setup_button(PIN_DPAD_RIGHT)

share = setup_button(PIN_SHARE)
options = setup_button(PIN_OPTIONS)
home = setup_button(PIN_HOME)
l1 = setup_button(PIN_L1)
r1 = setup_button(PIN_R1)

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
print("Botoes:")
print("Button 1 = SOUTH / X")
print("Button 2 = NORTH / B")
print("Button 3 = WEST  / A")
print("Button 4 = EAST  / Y")
print("Button 5 = SHARE")
print("Button 6 = OPTIONS")
print("Button 7 = HOME")
print("Button 8 = L1")
print("Button 9 = R1")
print("POV Hat = setas")
print()

last_buttons = None
last_hat = None
last_x = None
last_y = None
last_print_time = 0


# -------------------------------------------------------------------
# LOOP PRINCIPAL
# -------------------------------------------------------------------

while True:
    button_mask = 0

    # Botões principais
    if not south_x.value:
        button_mask |= 1 << 0  # Button 1 = SOUTH / X

    if not north_b.value:
        button_mask |= 1 << 1  # Button 2 = NORTH / B

    if not west_a.value:
        button_mask |= 1 << 2  # Button 3 = WEST / A

    if not east_y.value:
        button_mask |= 1 << 3  # Button 4 = EAST / Y

    # Botões extras
    if not share.value:
        button_mask |= 1 << 4  # Button 5 = SHARE

    if not options.value:
        button_mask |= 1 << 5  # Button 6 = OPTIONS

    if not home.value:
        button_mask |= 1 << 6  # Button 7 = HOME

    if not l1.value:
        button_mask |= 1 << 7  # Button 8 = L1

    if not r1.value:
        button_mask |= 1 << 8  # Button 9 = R1

    # Setas / POV Hat
    up_pressed = not dpad_up.value
    down_pressed = not dpad_down.value
    left_pressed = not dpad_left.value
    right_pressed = not dpad_right.value

    hat = read_hat(
        up_pressed,
        down_pressed,
        left_pressed,
        right_pressed
    )

    raw_x = axis_x.value
    raw_y = axis_y.value

    filtered_x = apply_smoothing(filtered_x, raw_x)
    filtered_y = apply_smoothing(filtered_y, raw_y)

    x = convert_axis(
        filtered_x,
        center_x,
        AXIS_X_MIN,
        AXIS_X_MAX,
        invert=INVERT_X
    )

    y = convert_axis(
        filtered_y,
        center_y,
        AXIS_Y_MIN,
        AXIS_Y_MAX,
        invert=INVERT_Y
    )

    if (
        button_mask != last_buttons
        or hat != last_hat
        or x != last_x
        or y != last_y
    ):
        gamepad.send_state(button_mask, hat, x, y)

        last_buttons = button_mask
        last_hat = hat
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
            "HID_RZ:", y,
            "| Buttons:", bin(button_mask),
            "| Hat:", hat
        )

    time.sleep(LOOP_DELAY)