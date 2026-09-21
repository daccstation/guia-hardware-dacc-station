# Lista de Materiais — Controle DACC Station

Este documento apresenta os materiais necessários para a reprodução do protótipo funcional do controle desenvolvido para o DACC Station.

> Esta lista contempla apenas o controle. A versão documentada utiliza comunicação **USB HID cabeada**. Embora a Nice!Nano/nRF52840 possua suporte a Bluetooth, a comunicação sem fio não foi concluída nesta versão do firmware.

---

## 1. Componentes eletrônicos

| Componente | Especificação | Quantidade | Função |
|---|---|---:|---|
| Nice!Nano | Placa baseada no microcontrolador nRF52840 | 1 | Leitura das entradas e comunicação USB HID com o console |
| Módulo joystick analógico | Joystick de 2 eixos, aproximadamente 34 × 26 mm | 1 | Entrada analógica para controle direcional |
| Push button | Botão de pressão momentâneo | 13 | Entradas digitais do controle |
| placa com fendas | Placa para prototipagem soldável, dimensionada para acomodar os 13 botões | 1 | Fixação mecânica dos botões e suporte às soldas dos jumpers |
| Placa de ensaio estreita | Matriz de 25 × 2 pontos (50 furos) | 1 | Barramento comum para GND dos botões e do joystick |
| Jumpers/fios de conexão | Compatíveis com os terminais dos componentes e da Nice!Nano | Conforme necessário | Interligação elétrica dos componentes |
| Cabo USB de dados | Compatível com a Nice!Nano e o Raspberry Pi | 1 | Alimentação e comunicação USB HID |

> A indicação **25 × 2 pontos** descreve a disposição física da placa de ensaio utilizada: 25 posições no comprimento e 2 no sentido transversal, totalizando 50 furos/pontos. Caso seja utilizado outro modelo, ele deve oferecer pontos suficientes para realizar o barramento de GND e caber no interior da carcaça.

---

## 2. Módulo joystick analógico

O controle utiliza um módulo joystick analógico de dois eixos.

O modelo considerado possui aproximadamente:

| Característica | Valor aproximado |
|---|---:|
| Comprimento da placa | 34 mm |
| Largura da placa | 26 mm |
| Altura do conjunto analógico | 12 mm |
| Diâmetro da base do botão | 27 mm |
| Diâmetro superior do botão | 18 mm |
| Curso/altura do eixo | 7 mm |

Na montagem utilizada, as conexões do módulo são:

- alimentação/VCC do módulo → VCC da Nice!Nano;
- GND → barramento de GND na placa de ensaio;
- eixo X → AIN0 / P0.02 da Nice!Nano;
- eixo Y → AIN5 / P0.29 da Nice!Nano.

As saídas analógicas dos eixos são processadas pelo microcontrolador do controle.

---

## 3. Botões

São utilizados **13 push buttons momentâneos** para as entradas digitais do controle.

Os botões são fixados em uma **placa com fendas**, que funciona como suporte mecânico para manter o alinhamento entre eles. Um jumper é soldado a um dos terminais de cada botão e conectado ao GPIO correspondente da Nice!Nano. Os terminais negativos/comuns são ligados ao barramento de GND montado na placa de ensaio de 25 × 2 pontos.

A pinagem definitiva é documentada nas instruções de montagem e no firmware.

---

## 4. Unidade de processamento

O controle utiliza uma placa **Nice!Nano**, baseada no microcontrolador **nRF52840**.

A placa é responsável por:

- leitura dos botões;
- leitura dos eixos do joystick;
- processamento das entradas;
- transmissão dos comandos para o Raspberry Pi por USB HID.

Embora o nRF52840 ofereça suporte a Bluetooth Low Energy, não foi possível concluir uma implementação funcional de Bluetooth HID na versão documentada. Por esse motivo, o protótipo funcional utiliza conexão USB cabeada.

Para reduzir a altura ocupada pela placa dentro da carcaça, os pinos laterais da Nice!Nano são dobrados aproximadamente 90° para fora: os pinos do lado direito são dobrados para a direita e os do lado esquerdo para a esquerda.

---

## 5. Distribuição de GND

Foi utilizada uma **placa de ensaio estreita de 25 × 2 pontos** como barramento comum de terra.

Nela são conectados:

- um ou mais jumpers provenientes de GND da Nice!Nano;
- os terminais negativos/comuns dos 13 botões;
- o GND do módulo joystick analógico.

Essa solução reduz a quantidade de conexões diretamente nos pinos de GND da Nice!Nano e facilita a organização interna dos fios.

---

## 6. Estrutura física

O gabinete do controle é produzido por impressão 3D a partir de um modelo tridimensional desenvolvido especificamente para acomodar:

- Nice!Nano;
- joystick analógico;
- placa com fendas com os 13 push buttons;
- placa de ensaio para distribuição de GND;
- fios e conexões internas.

### Materiais

| Componente | Quantidade | Função |
|---|---:|---|
| Carcaça impressa em 3D | 1 conjunto | Estrutura física do controle |
| Parafusos/elementos de fixação | Conforme modelo | Fechamento e montagem do gabinete |

A placa com fendas com os botões é encaixada na carcaça por **snap-fit**. O fechamento final é realizado pela parte superior da carcaça e pelos parafusos previstos no modelo.

---

## 7. Estrutura eletrônica

A versão funcional utiliza montagem prototipada com **placa com fendas, jumpers soldados e uma pequena placa de ensaio para distribuição do GND**. Essa solução foi adotada após dificuldades encontradas na fabricação artesanal da placa de circuito impresso inicialmente projetada.

A produção de uma PCB definitiva permanece como possibilidade de evolução do controle.

---

## 8. Resumo da lista de materiais

| Item | Quantidade |
|---|---:|
| Nice!Nano / nRF52840 | 1 |
| Módulo joystick analógico de 2 eixos | 1 |
| Push buttons | 13 |
| placa com fendas para os botões | 1 |
| Placa de ensaio 25 × 2 pontos | 1 |
| Jumpers/fios | Conforme necessário |
| Cabo USB de dados | 1 |
| Carcaça impressa em 3D | 1 conjunto |
| Parafusos/elementos de fixação | Conforme necessário |

---
