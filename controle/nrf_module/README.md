# nice!nano CircuitPython USB HID Gamepad mínimo

Arquivos necessários na raiz da unidade CIRCUITPY:

- boot.py
- code.py
- hid_gamepad.py

## Botões

Ligue cada botão entre um pino e GND.

Mapeamento padrão no code.py:

- SOUTH = X = board.D2
- NORTH = B = board.D3
- WEST  = A = board.D4
- EAST  = Y = board.D5

Se algum pino não existir, abra o REPL e rode:

import board
dir(board)

Depois altere os pinos no começo do code.py.

## Teste no Linux/Raspberry Pi

sudo apt install joystick
jstest /dev/input/js0

Ou:

sudo apt install evtest
sudo evtest
