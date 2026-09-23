# Firmware USB HID — Controle DACC Station

Este diretório contém os arquivos **efetivamente utilizados no protótipo atual** do controle DACC Station com Nice!Nano/nRF52840 e CircuitPython.

Arquivos principais a serem copiados para a raiz da unidade `CIRCUITPY`:

- `boot.py`
- `code.py`
- `hid_gamepad.py`
- `lib/`

A versão documentada foi utilizada com **CircuitPython 10.2.1** para `nice_nano`.

## Estrutura HID definida em `boot.py`

O firmware apresenta a Nice!Nano como um **USB HID Gamepad** com:

- 17 botões lógicos (`Button 1..17`, observados como `b0..b16`);
- D-Pad transmitido como quatro botões independentes (`b12..b15`);
- quatro eixos HID assinados de 8 bits: `X`, `Y`, `Z` e `Rx`, na faixa `-127..127`;
- relatório de entrada com 7 bytes: 3 bytes para os 17 bits de botões e 4 bytes para os eixos;
- nome de interface HID `DACC Station Joystick`.

O descritor mantém `X` e `Y` centralizados e utiliza `Z` e `Rx` para o único joystick físico. Assim, no host são enumerados quatro eixos, enquanto o joystick do protótipo ocupa os dois últimos.

## Índices utilizados pelo firmware

A classe `Gamepad` em `hid_gamepad.py` utiliza os seguintes índices:

| Constante no firmware | Índice HID |
|---|---:|
| `SOUTH_X` | `b0` |
| `NORTH_B` | `b1` |
| `WEST_A` | `b2` |
| `EAST_Y` | `b3` |
| `L1` | `b4` |
| `R1` | `b5` |
| `SHARE` | `b8` |
| `OPTIONS` | `b9` |
| `DPAD_UP` | `b12` |
| `DPAD_DOWN` | `b13` |
| `DPAD_LEFT` | `b14` |
| `DPAD_RIGHT` | `b15` |
| `HOME` | `b16` |

Os índices `b6`, `b7`, `b10` e `b11` permanecem sem entrada física na versão atual.

> **Importante:** os nomes `SOUTH_X`, `NORTH_B`, `WEST_A` e `EAST_Y` são nomes internos mantidos no firmware. A semântica final apresentada aos jogos é definida pela camada Linux `uinput`, validada em Steam e Godot. No gamepad virtual, `b0→A`, `b1→B`, `b2→Y` e `b3→X`.

## Pinagem utilizada por `code.py`

| Entrada | Constante | Pino Nice!Nano | Índice HID | Semântica final no gamepad virtual |
|---|---|---|---:|---|
| Botão 1 | `PIN_SOUTH_X` | `P1_11` | `b0` | A / `BTN_SOUTH` |
| Botão 2 | `PIN_NORTH_B` | `P0_10` | `b1` | B / `BTN_EAST` |
| Botão 3 | `PIN_WEST_A` | `P0_09` | `b2` | Y / `BTN_NORTH` |
| Botão 4 | `PIN_EAST_Y` | `P1_13` | `b3` | X / `BTN_WEST` |
| L1 | `PIN_L1` | `P0_20` | `b4` | `BTN_TL` |
| R1 | `PIN_R1` | `P0_22` | `b5` | `BTN_TR` |
| Share | `PIN_SHARE` | `P0_06` | `b8` | Back / `BTN_SELECT` |
| Options | `PIN_OPTIONS` | `P0_08` | `b9` | Start / `BTN_START` |
| D-Pad Up | `PIN_DPAD_UP` | `P1_00` | `b12` | `ABS_HAT0Y=-1` |
| D-Pad Down | `PIN_DPAD_DOWN` | `P0_11` | `b13` | `ABS_HAT0Y=1` |
| D-Pad Left | `PIN_DPAD_LEFT` | `P1_04` | `b14` | `ABS_HAT0X=-1` |
| D-Pad Right | `PIN_DPAD_RIGHT` | `P1_06` | `b15` | `ABS_HAT0X=1` |
| Home | `PIN_HOME` | `P0_17` | `b16` | Guide / `BTN_MODE` |
| Joystick X | `PIN_AXIS_X` | `AIN0 / P0_02` | `Z` | `ABS_RX` |
| Joystick Y | `PIN_AXIS_Y` | `AIN5 / P0_29` | `Rx` | `ABS_RY` |

Cada botão é configurado como entrada com `Pull.UP` e deve ser ligado entre o GPIO correspondente e o GND comum.

## Tratamento do joystick em `code.py`

A versão atual utiliza:

```text
DEADZONE = 42
SMOOTHING = 0.60
INVERT_X = False
INVERT_Y = False
AXIS_X_MIN = 0
AXIS_X_MAX = 51200
AXIS_Y_MIN = 0
AXIS_Y_MAX = 51200
LOOP_DELAY = 0.01 s
```

O centro dos dois eixos é calibrado automaticamente na inicialização a partir de 100 amostras. Portanto, mantenha o joystick parado no centro durante o início do firmware.

Depois da calibração, os valores são suavizados, normalizados para `-127..127`, submetidos à deadzone e enviados como `Z/Rx`. `X/Y` são enviados sempre como zero por `hid_gamepad.py`.

## Teste bruto no Linux

Para inspecionar o HID físico antes da camada `uinput`:

```bash
sudo evtest
```

No protótipo validado, o Linux identificou o dispositivo com VID `239a`, PID `80b4`, 17 eventos de botão e quatro eixos `ABS_X`, `ABS_Y`, `ABS_Z` e `ABS_RX`.

Para o uso normal no DACC Station, consulte [`../linux/dacc-gamepad/README.md`](../linux/dacc-gamepad/README.md).
