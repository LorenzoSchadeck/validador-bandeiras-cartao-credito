# Validador de Bandeiras de Cartão de Crédito

Aplicação desktop desenvolvida em **Python + Tkinter** capaz de identificar a bandeira de um cartão de crédito em tempo real e validar o número utilizando o **algoritmo de Luhn**.

Projeto desenvolvido com o auxílio do **GitHub Copilot** como assistente de codificação.

---

## Demonstração

| Ação | Resultado |
|---|---|
| Digitar / colar um número | Bandeira detectada instantaneamente com a cor da marca |
| Número completo e válido | ✓ Número válido (verde) |
| Número completo e inválido | ✗ Número inválido (vermelho) |
| Barra de progresso | Avança conforme o comprimento esperado da bandeira |

---

## Bandeiras Suportadas

| Bandeira | Prefixos / Ranges | Comprimento |
|---|---|---|
| Visa | 4 | 13 ou 16 dígitos |
| MasterCard | 51–55 · 2221–2720 | 16 dígitos |
| American Express | 34 · 37 | 15 dígitos |
| Diners Club | 300–305 · 36 · 38 | 14 dígitos |
| Discover | 6011 · 622126–622925 · 644–649 · 65 | 16 dígitos |
| EnRoute | 2014 · 2149 | 15 dígitos |
| JCB | 3528–3589 | 16 dígitos |
| Voyager | 8699 | 15 dígitos |
| HiperCard | 6062 · 3841 | 16 dígitos |
| Aura | 50 | 16 dígitos |

---

## Pré-requisitos

- Python 3.10 ou superior
- Tkinter (incluso na instalação padrão do Python)

> Nenhuma dependência externa é necessária — `pip install` não é obrigatório.

---

## Como Executar

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/validador-bandeiras-cartao-credito.git
cd validador-bandeiras-cartao-credito

# Execute a aplicação
python main.py
```

---

## Estrutura do Projeto

```
validador-bandeiras-cartao-credito/
├── main.py          # Ponto de entrada — instancia e executa a GUI
├── gui.py           # Interface gráfica Tkinter com validação em tempo real
├── validator.py     # Lógica pura: detecção de bandeira + algoritmo de Luhn
└── README.md
```

### Responsabilidades

- **`validator.py`** — Funções `detect_brand()`, `luhn_check()` e `validate_card()`. Sem dependências de UI, facilmente testável de forma isolada.
- **`gui.py`** — Layout e eventos da janela. Usa `StringVar.trace_add` para reagir a cada keystroke. Suporta colar números com espaços, hífens ou outros separadores.
- **`main.py`** — Apenas instancia `App` e chama `mainloop()`.

---

## Números de Teste

| Bandeira | Número | Luhn |
|---|---|---|
| Visa | `4111111111111111` | ✓ |
| MasterCard | `5500005555555559` | ✓ |
| American Express | `371449635398431` | ✓ |
| Diners Club | `30569309025904` | ✓ |
| Discover | `6011111111111117` | ✓ |
| JCB | `3530111333300000` | ✓ |
| HiperCard | `6062826786276634` | ✓ |

---

## Algoritmo de Luhn

O [algoritmo de Luhn](https://pt.wikipedia.org/wiki/Algoritmo_de_Luhn) é utilizado para validar a integridade do número do cartão:

1. A partir do último dígito, percorre os dígitos da direita para a esquerda.
2. Os dígitos em posições ímpares (1ª, 3ª, 5ª...) são dobrados.
3. Se o resultado da dobra for maior que 9, subtrai-se 9.
4. Soma todos os dígitos.
5. Se o total for divisível por 10, o número é válido.

---

## Desenvolvimento com GitHub Copilot

Este projeto foi desenvolvido explorando o GitHub Copilot para:

- Sugestão das regras de prefixos por bandeira
- Implementação do algoritmo de Luhn
- Estruturação do layout Tkinter
- Geração de casos de teste

---

## Licença

MIT
