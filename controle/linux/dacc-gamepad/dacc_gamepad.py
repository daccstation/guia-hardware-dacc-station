#!/usr/bin/env python3

import time

from evdev import (
    InputDevice,
    UInput,
    AbsInfo,
    ecodes as e,
    list_devices,
)


PHYSICAL_VENDOR = 0x239A
PHYSICAL_PRODUCT = 0x80B4

VIRTUAL_NAME = "DACC Station Controller"


# ============================================================
# Entrada física confirmada pelo evtest
# ============================================================

B0  = e.BTN_SOUTH           # 304
B1  = e.BTN_EAST            # 305
B2  = e.BTN_C               # 306
B3  = e.BTN_NORTH           # 307
B4  = e.BTN_WEST            # 308
B5  = e.BTN_Z               # 309

B8  = e.BTN_TL2             # 312
B9  = e.BTN_TR2             # 313

B12 = e.BTN_MODE            # 316
B13 = e.BTN_THUMBL          # 317
B14 = e.BTN_THUMBR          # 318
B15 = 319

B16 = e.BTN_TRIGGER_HAPPY1  # 704


BUTTON_MAP = {
    B0: e.BTN_SOUTH,    # A
    B1: e.BTN_EAST,     # B
    B2: e.BTN_NORTH,    # Y
    B3: e.BTN_WEST,     # X

    B4: e.BTN_TL,       # LB
    B5: e.BTN_TR,       # RB

    B8: e.BTN_SELECT,   # Back
    B9: e.BTN_START,    # Start

    B16: e.BTN_MODE,    # Guide
}


AXIS = AbsInfo(
    value=0,
    min=-32768,
    max=32767,
    fuzz=0,
    flat=4096,
    resolution=0,
)

HAT = AbsInfo(
    value=0,
    min=-1,
    max=1,
    fuzz=0,
    flat=0,
    resolution=0,
)


CAPABILITIES = {
    e.EV_KEY: [
        e.BTN_SOUTH,
        e.BTN_EAST,
        e.BTN_WEST,
        e.BTN_NORTH,

        e.BTN_TL,
        e.BTN_TR,

        e.BTN_SELECT,
        e.BTN_START,
        e.BTN_MODE,
    ],

    e.EV_ABS: [
        (e.ABS_X, AXIS),
        (e.ABS_Y, AXIS),

        (e.ABS_RX, AXIS),
        (e.ABS_RY, AXIS),

        (e.ABS_HAT0X, HAT),
        (e.ABS_HAT0Y, HAT),
    ],
}


dpad_up = False
dpad_down = False
dpad_left = False
dpad_right = False


def find_controller():
    for path in list_devices():
        try:
            dev = InputDevice(path)

            if (
                dev.info.vendor == PHYSICAL_VENDOR
                and dev.info.product == PHYSICAL_PRODUCT
                and dev.name != VIRTUAL_NAME
            ):
                return dev

            dev.close()

        except OSError:
            pass

    return None


def scale_axis(value):
    # Seu dispositivo físico já entrega -127..127.
    # Converte para aproximadamente -32768..32767.

    value = max(-127, min(127, value))

    if value >= 0:
        return int(value * 32767 / 127)

    return int(value * 32768 / 127)


def emit_dpad(ui):
    x = 0
    y = 0

    if dpad_left and not dpad_right:
        x = -1
    elif dpad_right and not dpad_left:
        x = 1

    if dpad_up and not dpad_down:
        y = -1
    elif dpad_down and not dpad_up:
        y = 1

    ui.write(e.EV_ABS, e.ABS_HAT0X, x)
    ui.write(e.EV_ABS, e.ABS_HAT0Y, y)
    ui.syn()


def process(dev, ui, event):
    global dpad_up
    global dpad_down
    global dpad_left
    global dpad_right

    # ========================================================
    # Botões
    # ========================================================

    if event.type == e.EV_KEY:

        pressed = event.value != 0

        # D-pad
        if event.code == B12:
            dpad_up = pressed
            emit_dpad(ui)
            return

        if event.code == B13:
            dpad_down = pressed
            emit_dpad(ui)
            return

        if event.code == B14:
            dpad_left = pressed
            emit_dpad(ui)
            return

        if event.code == B15:
            dpad_right = pressed
            emit_dpad(ui)
            return

        # Demais botões
        destination = BUTTON_MAP.get(event.code)

        if destination is not None:
            ui.write(
                e.EV_KEY,
                destination,
                1 if pressed else 0
            )
            ui.syn()

        return

    # ========================================================
    # Eixos
    #
    # Físico:
    #
    # ABS_X  = Left X
    # ABS_Y  = Left Y
    # ABS_Z  = Right X
    # ABS_RX = Right Y
    #
    # Virtual:
    #
    # ABS_X  = Left X
    # ABS_Y  = Left Y
    # ABS_RX = Right X
    # ABS_RY = Right Y
    # ========================================================

    if event.type == e.EV_ABS:

        if event.code == e.ABS_X:
            ui.write(
                e.EV_ABS,
                e.ABS_X,
                scale_axis(event.value)
            )
            ui.syn()
            return

        if event.code == e.ABS_Y:
            ui.write(
                e.EV_ABS,
                e.ABS_Y,
                scale_axis(event.value)
            )
            ui.syn()
            return

        if event.code == e.ABS_Z:
            ui.write(
                e.EV_ABS,
                e.ABS_RX,
                scale_axis(event.value)
            )
            ui.syn()
            return

        if event.code == e.ABS_RX:
            ui.write(
                e.EV_ABS,
                e.ABS_RY,
                scale_axis(event.value)
            )
            ui.syn()
            return


def reset_controller(ui):
    global dpad_up
    global dpad_down
    global dpad_left
    global dpad_right

    for button in [
        e.BTN_SOUTH,
        e.BTN_EAST,
        e.BTN_WEST,
        e.BTN_NORTH,
        e.BTN_TL,
        e.BTN_TR,
        e.BTN_SELECT,
        e.BTN_START,
        e.BTN_MODE,
    ]:
        ui.write(e.EV_KEY, button, 0)

    for axis in [
        e.ABS_X,
        e.ABS_Y,
        e.ABS_RX,
        e.ABS_RY,
        e.ABS_HAT0X,
        e.ABS_HAT0Y,
    ]:
        ui.write(e.EV_ABS, axis, 0)

    dpad_up = False
    dpad_down = False
    dpad_left = False
    dpad_right = False

    ui.syn()


def main():

    print("[DACC] Criando dispositivo virtual")

    with UInput(
        CAPABILITIES,
        name=VIRTUAL_NAME,
        vendor=0xDACC,
        product=0x0001,
        version=0x0001,
        bustype=e.BUS_USB,
        phys="dacc-station/uinput",
    ) as ui:

        print(
            f"[DACC] Criado: {VIRTUAL_NAME}"
        )

        reset_controller(ui)

        while True:

            dev = find_controller()

            if dev is None:
                print("[DACC] Aguardando nice!nano...")
                time.sleep(1)
                continue

            print(
                f"[DACC] Controle encontrado: "
                f"{dev.path} - {dev.name}"
            )

            try:
                # Impede que os jogos usem o HID original enquanto
                # o mapper está rodando.
                dev.grab()

                print("[DACC] HID físico capturado")

                reset_controller(ui)

                for event in dev.read_loop():
                    process(dev, ui, event)

            except OSError as exc:
                print(
                    f"[DACC] Controle desconectado: {exc}"
                )

            finally:
                try:
                    dev.ungrab()
                except Exception:
                    pass

                try:
                    dev.close()
                except Exception:
                    pass

                reset_controller(ui)

                time.sleep(1)


if __name__ == "__main__":
    main()
