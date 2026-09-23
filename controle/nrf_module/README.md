# Firmware USB HID — Controle DACC Station

Este diretório contém a versão do firmware CircuitPython utilizada pelo controle do DACC Station.

Arquivos principais a serem copiados para a raiz da unidade `CIRCUITPY`:

- `boot.py`
- `code.py`
- `hid_gamepad.py`
- `lib/`

A versão documentada foi testada com **CircuitPython 10.2.1** para `nice_nano`.

## Estrutura HID

O firmware apresenta a Nice!Nano como um **USB HID Gamepad** com:

- 17 posições lógicas de botão (`b0` a `b16`), das quais 13 correspondem a botões físicos;
- 4 eixos HID assinados: `X`, `Y`, `Z` e `Rx`;
- D-Pad transmitido como quatro botões independentes (`b12` a `b15`);
- joystick físico transmitido em `Z`/`Rx`.

O layout lógico utilizado é:

| Índice HID | Função física |
|---|---|
| `b0` | A |
| `b1` | B |
| `b2` | Y |
| `b3` | X |
| `b4` | L1 |
| `b5` | R1 |
| `b8` | Share / Back |
| `b9` | Options / Start |
| `b12` | D-Pad Up |
| `b13` | D-Pad Down |
| `b14` | D-Pad Left |
| `b15` | D-Pad Right |
| `b16` | Home / Guide |

Os índices `b6`, `b7`, `b10` e `b11` permanecem sem entrada física na versão atual.

## Joystick

O descritor HID expõe quatro eixos para manter uma estrutura de gamepad previsível:

- `X` e `Y`: permanecem centralizados;
- `Z`: eixo horizontal do joystick físico;
- `Rx`: eixo vertical do joystick físico.

No Linux, a camada `controle/linux/dacc-gamepad/` converte `Z/Rx` em `ABS_RX/ABS_RY`, apresentando o joystick como analógico direito do controle virtual.

## Pinagem utilizada

| Função | Pino Nice!Nano |
|---|---|
| A | `P1_11` |
| B | `P0_10` |
| Y | `P0_09` |
| X | `P1_13` |
| D-Pad Up | `P1_00` |
| D-Pad Down | `P0_11` |
| D-Pad Left | `P1_04` |
| D-Pad Right | `P1_06` |
| Share / Back | `P0_06` |
| Options / Start | `P0_08` |
| Home / Guide | `P0_17` |
| L1 | `P0_20` |
| R1 | `P0_22` |
| Joystick X | `AIN0` / `P0_02` |
| Joystick Y | `AIN5` / `P0_29` |

Cada botão é ligado entre o GPIO correspondente e `GND`, utilizando `Pull.UP` interno.

## Teste bruto no Linux

Para inspecionar o HID físico antes da camada `uinput`:

```bash
sudo evtest
```

No protótipo validado, o Linux identificou o dispositivo físico com VID `239a`, PID `80b4` e quatro eixos `ABS_X`, `ABS_Y`, `ABS_Z` e `ABS_RX`.

Para o uso normal no DACC Station, consulte [`../linux/dacc-gamepad/README.md`](../linux/dacc-gamepad/README.md).
