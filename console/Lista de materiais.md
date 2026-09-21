# Lista de Materiais — Console DACC Station

Este documento apresenta os materiais necessários para a reprodução do console do DACC Station.

> Esta lista contempla apenas o console.

---

## 1. Componentes principais

| Componente | Especificação | Quantidade | Função |
|---|---|---:|---|
| Raspberry Pi 4 Model B | 8 GB de RAM | 1 | Unidade computacional principal |
| Cartão microSD | 256 GB | 1 | Armazenamento do sistema operacional, middleware e jogos |
| Fonte de alimentação USB-C | 15 W | 1 | Alimentação do Raspberry Pi |
| Ventoinha | 5 V, 30 × 30 mm ou 40 × 40 mm| 1 | Refrigeração ativa |
| Dissipador de calor | 14 × 14 × 6 mm | 1 | Dissipação térmica dos componentes |
| Dissipador de calor | 9 × 9 × 5 mm | 2 | Dissipação térmica dos componentes |
| Dissipador de calor | 11 × 11 × 5 mm | 1 | Dissipação térmica dos componentes |
| Cabo micro-HDMI para HDMI | HDMI 2.0 | 1 | Conexão do console a monitor ou televisão |
| Espaçadores hexagonais | 12 mm de altura | 4 | Fixação do Raspberry Pi ao gabinete |

---

## 2. Gabinete

O gabinete do DACC Station é produzido por impressão 3D a partir do modelo desenvolvido no Blender.

### Especificações

| Característica | Valor |
|---|---|
| Material | PLA |
| Preenchimento (*infill*) | 100% |
| Impressora utilizada | Bambu Lab A1 |
| Filamento estimado | 40,79 g |
| Comprimento de filamento estimado | 13,68 m |
| Tempo estimado de impressão | 1 h 42 min |
| Dimensões aproximadas | 9 × 6 × 3 cm |

Os arquivos de modelagem e fabricação estão disponibilizados no diretório correspondente ao gabinete.

```text
console/
└── modelos_3d/
    ├── case_raspberry_base.stl
    ├── case_raspberry_topo.stl
    └── 