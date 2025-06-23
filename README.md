# Resumo Automático com T5

Projeto de geração de resumo automático usando o modelo `unicamp-dl/ptt5-base-portuguese-vocab`, baseado na arquitetura T5, com suporte à língua portuguesa. Utiliza a biblioteca `transformers` da Hugging Face.

---

## Membros do Grupo

- Miguel Carvalho Soares  
- Jonatas Mathias Dalló

---

## Funções

### `carregar_modelo`

Carrega o modelo T5 pré-treinado e configura o idioma para português.

- Detecta automaticamente o uso de CPU ou GPU.
- Carrega o tokenizer correspondente.
- Usa o modelo da Unicamp adaptado ao vocabulário em português.

---

### `resumir`

Gera um resumo abstrativo para um texto fornecido em português.

**Parâmetros:**

- `model`: instância carregada do T5  
- `tokenizer`: tokenizer configurado  
- `device`: `"cpu"` ou `"cuda"`  
- `texto`: texto de entrada  
- `max_length`: comprimento máximo do resumo  
- `min_length`: comprimento mínimo do resumo  
- `num_beams`: número de feixes (beam search)

---

### `preprocessar_texto`

Realiza uma limpeza e normalização básica do texto de entrada antes de gerar o resumo.

**Etapas de pré-processamento incluem:**

- Remoção de tabulações (`\t`)
- Substituição de caracteres especiais (como `‑` e ` `)
- Remoção de múltiplos espaços e quebras de linha redundantes
- Remoção de URLs e tags HTML
- Limpeza de espaços no início e fim do texto

---

### `gerar_estatisticas_simples`

Exibe estatísticas básicas sobre o processo de sumarização.

**Inclui:**

- Contagem de palavras do texto original  
- Contagem de palavras do resumo  
- Taxa de compressão (% de redução do texto)

---

## Execução

1. Coloque o texto desejado no arquivo `texto_original.txt`.
2. Instale as dependencias com pip install (use venv caso não queira instalar globalmente)
3. Por fim use o comando python main

---

## Video de Explicação
- [Clique Aqui!](https://www.youtube.com/watch?v=sqBBRNDe1fk)
