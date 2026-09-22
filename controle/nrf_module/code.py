# code.py
# Controle USB HID básico para nice!nano:
# - botoes principais + D-Pad como botoes
# - 1 analógico direito em Z/Rx (axes 2/3 no Windows)
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
# OBS: pinos corrigidos em relação à primeira versão. O teste no
# hardwaretester.com/gamepad mostrou que south estava fisicamente
# ligado ao pino de west, e north ao de east. Trocado aqui.

PIN_SOUTH_X = board.P1_11
PIN_NORTH_B = board.P0_10
PIN_WEST_A = board.P0_09
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
INVERT_Y = False  # era True; estava invertendo frente/tras

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
print("Button 5 = L1")
print("Button 6 = R1")
print("b8  = SHARE")
print("b9  = OPTIONS")
print("b12 = DPAD UP")
print("b13 = DPAD DOWN")
print("b14 = DPAD LEFT")
print("b15 = DPAD RIGHT")
print("b16 = HOME")
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

    # Botões principais (face)
    if not south_x.value:
        button_mask |= 1 << Gamepad.SOUTH_X  # b0 = SOUTH / X

    if not north_b.value:
        button_mask |= 1 << Gamepad.NORTH_B  # b1 = NORTH / B

    if not west_a.value:
        button_mask |= 1 << Gamepad.WEST_A  # b2 = WEST / A

    if not east_y.value:
        button_mask |= 1 << Gamepad.EAST_Y  # b3 = EAST / Y

    # Ombros
    if not l1.value:
        button_mask |= 1 << Gamepad.L1  # b4 = L1

    if not r1.value:
        button_mask |= 1 << Gamepad.R1  # b5 = R1

    # Menu
    if not share.value:
        button_mask |= 1 << Gamepad.SHARE  # b8 = SHARE

    if not options.value:
        button_mask |= 1 << Gamepad.OPTIONS  # b9 = OPTIONS

    # Home / Guide
    if not home.value:
        button_mask |= 1 << Gamepad.HOME  # b16 = HOME

    # D-Pad como botoes independentes
    if not dpad_up.value:
        button_mask |= 1 << Gamepad.DPAD_UP      # b12

    if not dpad_down.value:
        button_mask |= 1 << Gamepad.DPAD_DOWN    # b13

    if not dpad_left.value:
        button_mask |= 1 << Gamepad.DPAD_LEFT    # b14

    if not dpad_right.value:
        button_mask |= 1 << Gamepad.DPAD_RIGHT   # b15

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
        or x != last_x
        or y != last_y
    ):
        gamepad.send_state(button_mask, x, y)

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
            "| RIGHT_X(Z):", x,
            "RIGHT_Y(Rx):", y,
            "| Buttons:", bin(button_mask)
        )

    time.sleep(LOOP_DELAY)
