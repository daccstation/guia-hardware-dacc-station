# DACC Station Controller — Camada de compatibilidade Linux

Este diretório contém a camada de compatibilidade utilizada para transformar o HID USB do controle físico do DACC Station em um gamepad Linux com semântica padronizada.

A solução não implementa XInput no microcontrolador. O firmware permanece como **USB HID genérico** e o próprio sistema Linux realiza a tradução por meio de `evdev` e `uinput`.

## Arquitetura

```text
nice!nano / USB HID físico
        ↓
/dev/input/eventX (evdev)
        ↓
dacc_gamepad.py
        ↓
/dev/uinput
        ↓
DACC Station Controller
        ↓
SDL / Godot / Steam / jogos
```

A camada foi validada manualmente em **Fedora Linux**, com reconhecimento correto no `evtest`, na Steam em modo Big Picture e no Godot. A integração automática por `udev`/`systemd` e a posterior integração ao NixOS devem ser validadas no ambiente final antes de serem consideradas concluídas.

## Identificação do controle físico

No teste com `evtest`, o dispositivo apresentou:

```text
Bus:     0x3 (USB)
Vendor:  0x239a
Product: 0x80b4
Version: 0x0111
Name:    Nice Keyboards nice!nano
```

O mapper localiza o controle principalmente por **VID/PID**, sem depender de caminhos dinâmicos como `/dev/input/event4`.

## Eventos físicos confirmados

O HID atual expõe 17 botões lógicos e quatro eixos:

| Índice HID | Evento Linux físico | Uso no DACC Station |
|---|---|---|
| `b0` | `BTN_SOUTH` (304) | A |
| `b1` | `BTN_EAST` (305) | B |
| `b2` | `BTN_C` (306) | Y |
| `b3` | `BTN_NORTH` (307) | X |
| `b4` | `BTN_WEST` (308) | L1 |
| `b5` | `BTN_Z` (309) | R1 |
| `b8` | `BTN_TL2` (312) | Back / Share |
| `b9` | `BTN_TR2` (313) | Start / Options |
| `b12` | `BTN_MODE` (316) | D-Pad Up |
| `b13` | `BTN_THUMBL` (317) | D-Pad Down |
| `b14` | `BTN_THUMBR` (318) | D-Pad Left |
| `b15` | código `319` | D-Pad Right |
| `b16` | `BTN_TRIGGER_HAPPY1` (704) | Home / Guide |

Os índices `b6`, `b7`, `b10` e `b11` existem no descritor, mas não possuem entrada física na versão atual.

Os eixos físicos são:

```text
ABS_X   -127..127
ABS_Y   -127..127
ABS_Z   -127..127
ABS_RX  -127..127
```

O joystick físico atual utiliza `ABS_Z` (horizontal) e `ABS_RX` (vertical). `ABS_X`/`ABS_Y` permanecem disponíveis e centralizados.

## Saída virtual

O `dacc_gamepad.py` cria:

```text
DACC Station Controller
VID virtual: 0xdacc
PID virtual: 0x0001
```

Esse VID/PID existe apenas no dispositivo virtual criado localmente pelo `uinput`; ele não representa uma identificação USB física registrada.

A saída expõe:

### Botões

| Entrada física | Saída virtual |
|---|---|
| A (`b0`) | `BTN_SOUTH` |
| B (`b1`) | `BTN_EAST` |
| X (`b3`) | `BTN_WEST` |
| Y (`b2`) | `BTN_NORTH` |
| L1 (`b4`) | `BTN_TL` |
| R1 (`b5`) | `BTN_TR` |
| Back (`b8`) | `BTN_SELECT` |
| Start (`b9`) | `BTN_START` |
| Home (`b16`) | `BTN_MODE` |

> O mapeamento X/Y acima já contém a correção validada nos testes em Steam e Godot: o X físico está em `b3` e o Y físico em `b2`.

### D-Pad

O D-Pad físico é convertido de quatro botões independentes para dois eixos Hat:

| Direção | Saída virtual |
|---|---|
| Cima | `ABS_HAT0Y = -1` |
| Baixo | `ABS_HAT0Y = 1` |
| Esquerda | `ABS_HAT0X = -1` |
| Direita | `ABS_HAT0X = 1` |
| Neutro | eixo correspondente = `0` |

### Analógico

| Evento físico | Saída virtual |
|---|---|
| `ABS_X` | `ABS_X` |
| `ABS_Y` | `ABS_Y` |
| `ABS_Z` | `ABS_RX` |
| `ABS_RX` | `ABS_RY` |

A saída virtual utiliza faixa `-32768..32767` para os analógicos e expõe `ABS_HAT0X/ABS_HAT0Y` com faixa `-1..1`.

## Arquivos

| Arquivo | Destino no sistema | Função |
|---|---|---|
| `dacc_gamepad.py` | `/usr/local/libexec/dacc-gamepad/dacc_gamepad.py` | Tradução `evdev → uinput` |
| `71-dacc-gamepad.rules` | `/etc/udev/rules.d/71-dacc-gamepad.rules` | Restringe o HID físico e classifica o virtual |
| `dacc-gamepad.service` | `/etc/systemd/system/dacc-gamepad.service` | Inicialização e reinício automático do mapper |
| `dacc-gamepad.conf` | `/etc/modules-load.d/dacc-gamepad.conf` | Carrega `uinput` durante o boot |

## Dependências no Fedora

```bash
sudo dnf install python3-evdev evtest
```

Carregue o módulo para o primeiro teste:

```bash
sudo modprobe uinput
ls -l /dev/uinput
```

## Teste manual — versão já validada

Antes de instalar `udev` e `systemd`, o mapper pode ser executado diretamente:

```bash
sudo python3 dacc_gamepad.py
```

Em outro terminal:

```bash
sudo evtest
```

Selecione `DACC Station Controller`. O dispositivo virtual esperado contém:

```text
BTN_SOUTH
BTN_EAST
BTN_NORTH
BTN_WEST
BTN_TL
BTN_TR
BTN_SELECT
BTN_START
BTN_MODE

ABS_X
ABS_Y
ABS_RX
ABS_RY
ABS_HAT0X
ABS_HAT0Y
```

Esse estágio foi validado em Fedora, Steam Big Picture e Godot.

## Instalação no Fedora

### 1. Instalar o mapper

```bash
sudo mkdir -p /usr/local/libexec/dacc-gamepad
sudo install -m 0755 dacc_gamepad.py \
  /usr/local/libexec/dacc-gamepad/dacc_gamepad.py
```

Confirme a dependência:

```bash
sudo /usr/bin/python3 -c "import evdev; print('evdev OK')"
```

### 2. Carregar `uinput` automaticamente

```bash
sudo install -m 0644 dacc-gamepad.conf \
  /etc/modules-load.d/dacc-gamepad.conf
sudo modprobe uinput
```

### 3. Instalar a regra `udev`

```bash
sudo install -m 0644 71-dacc-gamepad.rules \
  /etc/udev/rules.d/71-dacc-gamepad.rules
sudo udevadm control --reload-rules
```

Desconecte e reconecte fisicamente o controle para aplicar as regras ao dispositivo.

### 4. Instalar e iniciar o serviço

Encerre qualquer instância manual do mapper antes de continuar.

```bash
sudo install -m 0644 dacc-gamepad.service \
  /etc/systemd/system/dacc-gamepad.service
sudo systemctl daemon-reload
sudo systemctl enable --now dacc-gamepad.service
```

Verifique:

```bash
systemctl status dacc-gamepad.service
journalctl -u dacc-gamepad.service -f
```

## Testes recomendados após a instalação automática

1. Verifique que o serviço está `active (running)`.
2. Confirme que `DACC Station Controller` aparece no `evtest`.
3. Teste os 13 botões físicos e o joystick.
4. Desconecte o USB e confirme que o serviço continua ativo.
5. Reconecte e confirme a captura automática do novo `/dev/input/eventX`.
6. Reinicie o computador e confirme que o controle virtual existe sem executar scripts manualmente.
7. Teste novamente Steam Big Picture e Godot.


