# Configuração da Nice!Nano — Controle DACC Station

Este documento descreve o procedimento utilizado para preparar e configurar a placa Nice!Nano baseada no microcontrolador nRF52840 utilizada no controle do DACC Station.

> Antes de realizar qualquer conexão, verifique a identificação dos pinos da sua versão da Nice!Nano.
>
> O curto descrito neste documento deve ser realizado **somente entre RESET (RST) e GND**.
>
> Para reproduzir a configuração utilizada no protótipo do DACC Station, recomenda-se utilizar **CircuitPython 10.2.1**, versão registrada no arquivo `boot_out.txt` do módulo disponibilizado no repositório.

---

## 1. Materiais necessários

Para realizar a configuração são necessários:

- Nice!Nano ou placa compatível baseada no nRF52840;
- cabo USB com suporte a transmissão de dados;
- computador;
- acesso à página oficial do CircuitPython para a Nice!Nano;
- arquivos contidos no diretório `nrf_module` do repositório do DACC Station;
- pinça metálica, jumper ou outro condutor, caso a placa não possua botão de reset.

Página oficial do CircuitPython para a Nice!Nano:

<https://circuitpython.org/board/nice_nano/>

---

## 2. Conectando a placa ao computador

Conecte a Nice!Nano ao computador utilizando um cabo USB capaz de transmitir dados.

> Alguns cabos USB são destinados apenas à alimentação e não permitem comunicação com o computador.

Durante a configuração, recomenda-se manter os demais componentes externos desconectados da placa.

Depois de conectar a Nice!Nano, verifique se uma unidade chamada `CIRCUITPY` aparece no explorador de arquivos.

### Se `CIRCUITPY` já aparecer

O CircuitPython já está instalado na placa. Nesse caso, prossiga diretamente para a seção **6. Copiando o módulo do DACC Station**.

### Se `CIRCUITPY` não aparecer

Será necessário entrar no bootloader e instalar o CircuitPython, conforme descrito nas próximas seções.

---

## 3. Entrando no bootloader

Para instalar o CircuitPython, a Nice!Nano precisa ser iniciada no modo de bootloader. Nesse modo, a placa aparece no computador como uma unidade de armazenamento removível.

Existem duas formas de realizar o procedimento.

### 3.1. Placas com botão de reset

Caso a versão da Nice!Nano utilizada possua um botão de reset:

1. mantenha a placa conectada ao computador pelo cabo USB;
2. pressione o botão de reset **duas vezes rapidamente**;
3. aguarde alguns segundos;
4. uma nova unidade de armazenamento deverá aparecer no computador.

O nome da unidade pode variar de acordo com o bootloader instalado.

---

### 3.2. Placas sem botão de reset

Caso a placa não possua botão físico de reset, o procedimento pode ser realizado utilizando os contatos **RST** e **GND**.

Localize os pontos correspondentes a:

```text
RST
GND
```

Com a placa conectada ao computador, faça um contato momentâneo entre `RST` e `GND` **duas vezes rapidamente**.

Representação simplificada:

```text
RST ----- GND
```

O contato pode ser feito utilizando uma pinça metálica, jumper ou outro condutor apropriado.

> Não mantenha RST e GND conectados permanentemente. Cada contato deve ser apenas momentâneo.
>
> Não faça curto entre outros pinos da placa.

Após o segundo contato, aguarde alguns segundos. Uma nova unidade de armazenamento deverá aparecer no computador.

---

## 4. Verificando se o bootloader foi iniciado

Após realizar o duplo reset, verifique o explorador de arquivos do sistema operacional.

A Nice!Nano deverá aparecer como uma nova unidade removível. Essa unidade **não é a mesma unidade `CIRCUITPY`**; ela corresponde ao bootloader e é utilizada para instalar o firmware do CircuitPython.

No Linux, também é possível verificar as unidades conectadas utilizando:

```bash
lsblk
```

A presença da nova unidade indica que a placa entrou corretamente no modo de bootloader.

Se nenhuma unidade aparecer:

1. confirme que o cabo USB suporta transmissão de dados;
2. desconecte e reconecte a placa;
3. repita o duplo reset;
4. confirme que os contatos utilizados são realmente `RST` e `GND`.

---

## 5. Instalando o CircuitPython

A configuração utilizada no protótipo do DACC Station foi registrada com:

```text
Adafruit CircuitPython 10.2.1
nice!nano with nRF52840
Board ID: nice_nano
```

Para reproduzir o ambiente utilizado no projeto, recomenda-se instalar a mesma versão.

### 5.1. Baixando o firmware

Acesse:

<https://circuitpython.org/board/nice_nano/>

Localize a versão **CircuitPython 10.2.1** para a Nice!Nano e baixe o arquivo no formato `.uf2`.

O arquivo terá um nome semelhante a:

```text
adafruit-circuitpython-nice_nano-pt_BR-10.2.1.uf2
```

ou:

```text
adafruit-circuitpython-nice_nano-en_US-10.2.1.uf2
```

O idioma escolhido para o firmware não altera o funcionamento do controle.

### 5.2. Gravando o CircuitPython

Com a Nice!Nano no modo de bootloader:

1. abra a unidade removível correspondente ao bootloader;
2. copie o arquivo `.uf2` do CircuitPython para essa unidade;
3. aguarde a cópia ser concluída;
4. não desconecte a placa durante a gravação.

Depois que o arquivo for copiado, a Nice!Nano deverá reiniciar automaticamente.

A unidade do bootloader desaparecerá e, após alguns segundos, deverá surgir uma nova unidade chamada:

```text
CIRCUITPY
```

Essa unidade corresponde ao sistema de arquivos do CircuitPython e é onde os arquivos do controle serão instalados.

> Em placas nRF52840, versões recentes do CircuitPython exigem um bootloader UF2 compatível. Caso o arquivo `.uf2` não seja aceito ou a instalação falhe, verifique a versão do bootloader da placa antes de prosseguir.

---

## 6. Copiando o módulo do DACC Station

O repositório do DACC Station contém o diretório:

```text
nrf_module/
```

Esse diretório reúne os arquivos utilizados na configuração funcional do protótipo.

A estrutura fornecida inclui, entre outros:

```text
nrf_module/
├── boot.py
├── code.py
├── hid_gamepad.py
├── lib/
├── settings.toml
└── boot_out.txt
```

### 6.1. Faça backup do conteúdo atual

Antes de substituir os arquivos da unidade `CIRCUITPY`, recomenda-se copiar seu conteúdo atual para uma pasta de backup no computador.

Por exemplo:

```text
backup_circuitpy/
```

### 6.2. Copie os arquivos

Abra a pasta `nrf_module` no computador e copie **o conteúdo dela** para a raiz da unidade `CIRCUITPY`.

A estrutura final da unidade deverá ficar semelhante a:

```text
CIRCUITPY/
├── boot.py
├── code.py
├── hid_gamepad.py
├── lib/
├── settings.toml
└── ...
```

> Não copie a pasta `nrf_module` como uma subpasta dentro de `CIRCUITPY`. Copie os arquivos e diretórios que estão dentro dela diretamente para a raiz da unidade.

Caso o sistema pergunte se arquivos existentes devem ser substituídos, confirme a substituição dos arquivos correspondentes ao projeto.

A pasta `lib/` deve ser copiada juntamente com os scripts, pois contém bibliotecas utilizadas pelo ambiente do projeto.

---

## 7. Função dos principais arquivos

### `boot.py`

É executado durante a inicialização da placa e configura o dispositivo HID apresentado ao computador ou Raspberry Pi.

Na versão atualmente armazenada no repositório, o descritor HID define:

- até 13 botões HID;
- POV Hat utilizado pelo D-Pad;
- dois eixos analógicos;
- identificação do dispositivo como `DACC Station Joystick`.

### `code.py`

Contém a lógica principal de execução do controle, incluindo:

- leitura dos botões;
- leitura do D-Pad;
- leitura do joystick analógico;
- calibração automática do centro do joystick;
- aplicação de deadzone;
- suavização dos valores analógicos;
- conversão dos valores lidos;
- envio dos estados para o dispositivo HID.

### `hid_gamepad.py`

Implementa a estrutura utilizada para montar e enviar os relatórios HID do gamepad.

### `lib/`

Contém bibliotecas necessárias para o ambiente utilizado pelo projeto.

---

## 8. Reiniciando a placa após copiar os arquivos

Depois que todos os arquivos forem copiados para `CIRCUITPY`, reinicie a Nice!Nano.

O reset pode ser realizado de uma das seguintes formas:

- desconectar e reconectar o cabo USB;
- pressionar uma vez o botão de reset, quando disponível;
- realizar um único contato momentâneo entre `RST` e `GND`.

Após a reinicialização, o CircuitPython executará automaticamente o `boot.py` e, em seguida, o `code.py`.

---

## 9. Verificando a versão instalada

Dentro da unidade `CIRCUITPY`, o arquivo:

```text
boot_out.txt
```

registra informações sobre o CircuitPython instalado.

Para reproduzir a configuração utilizada no DACC Station, o conteúdo deve indicar uma versão equivalente a:

```text
Adafruit CircuitPython 10.2.1
nice!nano with nRF52840
Board ID: nice_nano
```

Pequenas diferenças de identificação podem ocorrer em placas compatíveis ou clones.

---

## 10. Testando a configuração

Antes de instalar definitivamente a Nice!Nano na carcaça do controle, realize um teste com a placa conectada ao computador por USB.

A versão atual do módulo do repositório configura a Nice!Nano como um **USB HID Gamepad**.

O dispositivo é identificado como:

```text
DACC Station Joystick
```

### 10.1. Teste no Linux ou Raspberry Pi

Uma opção é utilizar `jstest`.

Instale o pacote:

```bash
sudo apt install joystick
```

Verifique os dispositivos disponíveis:

```bash
ls /dev/input/js*
```

Em seguida:

```bash
jstest /dev/input/js0
```

Também é possível utilizar `evtest`:

```bash
sudo apt install evtest
sudo evtest
```

Selecione o dispositivo correspondente ao `DACC Station Joystick`.

Durante o teste, verifique:

- botões principais;
- D-Pad;
- joystick analógico;
- reconhecimento dos eixos;
- estabilidade do dispositivo.

---

## 11. Solução de problemas

### `CIRCUITPY` não aparece após conectar a placa

O CircuitPython pode não estar instalado ou a placa pode não ter inicializado corretamente.

Tente:

1. verificar o cabo USB;
2. entrar novamente no bootloader por duplo reset;
3. reinstalar o arquivo `.uf2` correspondente à Nice!Nano.

---

### A unidade do bootloader não aparece

Repita o duplo reset.

Com botão:

```text
RESET
RESET
```

Sem botão:

```text
RST -> GND
RST -> GND
```

Os dois acionamentos devem ocorrer rapidamente.

---

### O arquivo `.uf2` não instala

Verifique:

- se o firmware baixado corresponde à placa `nice_nano`;
- se o arquivo está no formato `.uf2`;
- se a unidade aberta corresponde realmente ao bootloader;
- se o bootloader UF2 da placa é compatível com a versão do CircuitPython utilizada.

---

### `CIRCUITPY` aparece, mas o controle não funciona

Verifique se os seguintes arquivos estão na raiz:

```text
boot.py
code.py
hid_gamepad.py
```

Verifique também se a pasta:

```text
lib/
```

foi copiada corretamente.

Reinicie completamente a placa depois de copiar os arquivos.

---

### O controle não é reconhecido como HID

Revise principalmente o arquivo:

```text
boot.py
```

Esse arquivo define o dispositivo HID apresentado pela Nice!Nano.

Após qualquer alteração no `boot.py`, reinicie completamente a placa.

---

### Erro relacionado a um pino

Caso seja utilizada uma versão diferente ou compatível da Nice!Nano, os nomes dos pinos disponíveis no CircuitPython podem variar.

No REPL do CircuitPython, é possível verificar os pinos disponíveis com:

```python
import board
dir(board)
```

Depois, compare os nomes disponíveis com os definidos no início do `code.py`.

---

## 12. Cuidados durante a configuração

- Faça curto somente entre `RST` e `GND`.
- Nunca faça curto entre alimentação e GND.
- Não mantenha `RST` e `GND` conectados continuamente.
- Configure a placa com os demais componentes externos desconectados sempre que possível.
- Utilize um cabo USB com transmissão de dados.
- Aguarde o término da gravação antes de desconectar a placa.
- Faça backup do conteúdo de `CIRCUITPY` antes de substituir arquivos.
- Realize os primeiros testes antes de fixar a placa permanentemente na carcaça.

---

## 13. Próxima etapa

Depois que a Nice!Nano estiver configurada e o funcionamento do dispositivo HID tiver sido validado, prossiga para as instruções de montagem física do controle:

```text
Instrucoes de montagem.md
```

Nesse documento estão descritos:

- posicionamento dos componentes;
- fixação dos componentes na carcaça;
- pinagem dos botões;
- conexão do D-Pad;
- conexão do joystick analógico;
- conexão do barramento de GND;
- fechamento e teste final do controle.