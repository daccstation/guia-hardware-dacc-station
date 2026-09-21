# DACC Station — Guia de Produção do Hardware

Este repositório reúne os arquivos e a documentação necessários para a reprodução do hardware do **DACC Station**, incluindo o console baseado em Raspberry Pi e o protótipo funcional do controle desenvolvido para o projeto.

O material foi organizado de forma a permitir a consulta separada dos componentes, arquivos de fabricação, instruções de montagem e configuração eletrônica.

> Este repositório concentra-se na **reprodução física do hardware**. A configuração do sistema operacional e da plataforma de distribuição de jogos do Raspberry Pi não é detalhada neste guia.

---

## Diagrama de arquitetura

![alt text](<console/Diagrama de arquitetura.jpg>)

---

# 1. Console

O console utiliza um **Raspberry Pi 4 Model B com 8 GB de RAM**, armazenamento em cartão microSD, refrigeração ativa e uma carcaça própria produzida por impressão 3D.

## Principais componentes

- Raspberry Pi 4 Model B — 8 GB;
- cartão microSD de 256 GB;
- fonte USB-C de 15 W;
- ventoinha de 30 × 30 mm ou 40 × 40 mm;
- dissipadores de calor;
- cabo micro-HDMI para HDMI;
- quatro espaçadores hexagonais de 12 mm;
- carcaça impressa em 3D.

A relação completa dos componentes está disponível em:

- [Lista de materiais do console](console/Lista%20de%20materiais.md)

## Arquivos de fabricação

Os modelos utilizados para fabricação do gabinete estão disponíveis em:

```text
console/modelos_3d/
```

Arquivos fornecidos:

- `case_raspberry_base.stl`
- `case_raspberry_topo.stl`

A carcaça utilizada no protótipo foi produzida em PLA, com preenchimento de 100%.

## Montagem

De forma resumida, a montagem do console consiste em:

1. imprimir as duas partes da carcaça;
2. posicionar o Raspberry Pi na base;
3. fixar a placa utilizando os espaçadores;
4. parafusar a ventoinha na parte superior da carcaça;
5. encaixar a parte superior sobre a base;
6. inserir os parafusos superiores e fixá-los nos espaçadores.

As instruções completas estão disponíveis em:

- [Instruções de montagem do console](console/Instrucoes%20de%20montagem.md)

---

# 2. Controle

O controle corresponde ao protótipo funcional desenvolvido para o DACC Station, utilizando uma placa **Nice!Nano baseada no nRF52840**, joystick analógico, 13 botões de pressão, placa com fendas e uma pequena placa de ensaio utilizada como barramento de GND.

Na versão documentada, a comunicação é realizada por **USB HID cabeado**. Os botões são fixados em uma placa com fendas, com jumpers soldados aos seus terminais, enquanto uma placa de ensaio estreita de **25 × 2 pontos** concentra as conexões de GND dos botões e do joystick. A placa com fendas é instalada na carcaça por encaixe **snap-fit**.

## Arquivos de fabricação

Os modelos utilizados para fabricação da carcaça do controle estão disponíveis em:

```text
controle/modelos_3d/
```

Arquivos fornecidos:

- `.stl`
- `.stl`

A carcaça utilizada no protótipo foi produzida em PLA, com preenchimento de 100%.

## Principais componentes

- Nice!Nano / nRF52840;
- módulo joystick analógico de dois eixos;
- botões de pressão;
- placa com fendas para fixação dos botões;
- placa de ensaio de 25 × 2 pontos para distribuição de GND;
- jumpers/fios para as conexões;
- cabo USB de dados;
- carcaça impressa em 3D;
- elementos de fixação.

A relação detalhada está disponível em:

- [Lista de materiais do controle](controle/Lista%20de%20materiais.md)

---

## 2.1. Configuração da Nice!Nano

Antes da montagem física do controle, a Nice!Nano deve ser configurada.

O protótipo documentado utiliza:

```text
Adafruit CircuitPython 10.2.1
nice!nano with nRF52840
Board ID: nice_nano
```

A página oficial do CircuitPython para a placa está disponível em:

<https://circuitpython.org/board/nice_nano/>

### Fluxo resumido

1. conecte a Nice!Nano ao computador utilizando um cabo USB de dados;
2. verifique se a unidade `CIRCUITPY` já está disponível;
3. caso não esteja, entre no bootloader utilizando o duplo reset;
4. instale o CircuitPython 10.2.1 para a Nice!Nano;
5. aguarde o aparecimento da unidade `CIRCUITPY`;
6. copie o conteúdo de `controle/nrf_module/` para a raiz da unidade `CIRCUITPY`;
7. reinicie a placa;
8. teste o dispositivo antes de instalá-lo definitivamente na carcaça.

### Entrada no bootloader

Se a placa possuir botão de reset, pressione-o **duas vezes rapidamente**.

Caso o modelo não possua botão, o mesmo procedimento pode ser realizado fazendo dois contatos momentâneos entre:

```text
RST ----- GND
```

> **Atenção:** faça contato somente entre `RST` e `GND`. Não faça curto entre outros pinos da placa.

O procedimento completo está disponível em:

- [Instruções de configuração da Nice!Nano](controle/Instrucoes%20de%20configuracao.md)

---

## 2.2. Firmware do controle

Os arquivos utilizados no protótipo estão disponíveis em:

```text
controle/nrf_module/
```

Os principais arquivos são:

| Arquivo | Função |
|---|---|
| `boot.py` | Configura o dispositivo HID apresentado ao sistema |
| `code.py` | Realiza a leitura das entradas e controla o funcionamento do gamepad |
| `hid_gamepad.py` | Monta e envia os relatórios HID |
| `lib/` | Bibliotecas utilizadas pelo ambiente do projeto |
| `settings.toml` | Arquivo de configuração do CircuitPython |
| `boot_out.txt` | Registro da versão do CircuitPython utilizada |

Na versão atualmente documentada, o dispositivo é configurado como um **USB HID Gamepad** identificado como:

```text
DACC Station Joystick
```

---

## 2.3. Montagem do controle

Depois de configurar e testar a Nice!Nano:

1. imprima a carcaça e teste os encaixes e parafusos;
2. fixe os 13 botões na placa com fendas e solde os jumpers;
3. dobre os pinos laterais da Nice!Nano em aproximadamente 90° para fora;
4. posicione a Nice!Nano no centro da parte inferior da carcaça;
5. conecte os jumpers dos botões aos GPIOs correspondentes;
6. utilize a placa de ensaio de 25 × 2 pontos como barramento comum para GND;
7. conecte o joystick ao VCC, ao barramento de GND e aos pinos analógicos X/Y;
8. teste todas as entradas antes do fechamento;
9. encaixe a placa com fendas na carcaça por snap-fit;
10. alinhe botões e joystick às aberturas, feche e parafuse a carcaça;
11. realize um novo teste funcional após o fechamento.

As conexões e a pinagem completa estão documentadas em:

- [Instruções de montagem do controle](controle/Instrucoes%20de%20montagem.md)

---

# 3. Teste do controle

Antes da montagem definitiva, recomenda-se testar a Nice!Nano conectada ao computador ou Raspberry Pi.

Em sistemas Linux, o controle pode ser verificado com `jstest`:

```bash
sudo apt install joystick
jstest /dev/input/js0
```

Também é possível utilizar `evtest`:

```bash
sudo apt install evtest
sudo evtest
```

Durante o teste, verifique:

- reconhecimento do dispositivo;
- botões principais;
- D-Pad;
- joystick analógico;
- leitura dos eixos;
- estabilidade do funcionamento.

---

# 4. Ordem recomendada para reprodução

Para reproduzir o conjunto completo, recomenda-se seguir esta ordem:

### Console

1. consultar a [lista de materiais](console/Lista%20de%20materiais.md);
2. imprimir os arquivos de `console/modelos_3d/`;
3. seguir as [instruções de montagem](console/Instrucoes%20de%20montagem.md).

### Controle

1. consultar a [lista de materiais](controle/Lista%20de%20materiais.md);
2. preparar a Nice!Nano conforme as [instruções de configuração](controle/Instrucoes%20de%20configuracao.md);
3. imprimir a carcaça do controle;
4. seguir as [instruções de montagem](controle/Instrucoes%20de%20montagem.md);
5. testar todas as entradas antes do fechamento definitivo.

---

# 5. Documentação disponível

| Documento | Conteúdo |
|---|---|
| [Lista de materiais do console](console/Lista%20de%20materiais.md) | Componentes e especificações do console |
| [Montagem do console](console/Instrucoes%20de%20montagem.md) | Montagem física do Raspberry Pi e da carcaça |
| [Lista de materiais do controle](controle/Lista%20de%20materiais.md) | Componentes necessários para o controle |
| [Configuração da Nice!Nano](controle/Instrucoes%20de%20configuracao.md) | Instalação do CircuitPython e do módulo do controle |
| [Montagem do controle](controle/Instrucoes%20de%20montagem.md) | Posicionamento, pinagem, conexões e montagem física |

---

# 6. Observações de reprodução

- Utilize um cabo USB com suporte a transmissão de dados durante a configuração da Nice!Nano.
- Para o protótipo documentado, recomenda-se utilizar o **CircuitPython 10.2.1**.
- Antes de substituir os arquivos da unidade `CIRCUITPY`, faça uma cópia de segurança do conteúdo existente.
- Teste a Nice!Nano antes de fixá-la dentro da carcaça.
- Verifique todas as conexões antes de conectar a Nice!Nano ao Raspberry Pi por USB.
- Não mantenha `RST` e `GND` conectados permanentemente.
- Evite aplicar força excessiva nos parafusos das peças impressas em 3D.
- Antes do fechamento de qualquer carcaça, confirme que fios e componentes não estão sendo pressionados ou deslocados.

---

# Sobre o DACC Station

O DACC Station é um projeto voltado ao desenvolvimento de uma plataforma física para execução e disponibilização de jogos produzidos no contexto do curso de Ciência da Computação da Universidade Federal de Rondônia (UNIR).

Este repositório documenta os elementos de hardware necessários para facilitar a reprodução do console e do controle desenvolvidos no projeto.
