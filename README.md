# Resumo Automático com mBART

Projeto de geração de resumo automático usando o modelo `facebook/mbart-large-50-many-to-many-mmt` da Meta (Facebook AI), com suporte à língua portuguesa. Utiliza a biblioteca `transformers` da Hugging Face.

---

## Membros do Grupo

- Miguel Carvalho Soares  
- Jonatas Mathias Dalló

---

## Funções

### `carregar_modelo()`

Carrega o modelo mBART pré-treinado e configura o idioma para português.

- Detecta automaticamente o uso de CPU ou GPU.
- Carrega o tokenizer correspondente.
- Define os idiomas de origem e destino como `pt_XX` (português).

---

### `resumir(modelo, tokenizer, device, texto: str, max_length=150, min_length=50, num_beams=5)`

Gera um resumo abstrativo para um texto fornecido em português.

**Parâmetros:**

- `modelo`: instância carregada do mBART
- `tokenizer`: tokenizer configurado
- `device`: `"cpu"` ou `"cuda"`
- `texto`: texto de entrada
- `max_length`: comprimento máximo do resumo
- `min_length`: comprimento mínimo do resumo
- `num_beams`: número de feixes (beam search)

---

### `preprocessar_texto(texto: str) -> str`

Realiza uma limpeza e normalização básica do texto de entrada antes de gerar o resumo.  
Remove tabulações, espaços duplicados, URLs, HTML, colchetes, e substitui certos caracteres.

**Etapas de pré-processamento incluem:**

- Remoção de tabulações (`\t`)
- Substituição de `;` por `.`
- Remoção de colchetes `[]`
- Remoção de múltiplos espaços
- Remoção de URLs e tags HTML
- Remoção de quebras de linha desnecessárias
- Strip final para limpar espaços no início/fim do texto

---

## Execução

1. Coloque o texto desejado no arquivo `texto_original.txt`.
2. Instale as dependencias com pip install (use venv caso não queira instalar globalmente)
3. Por fim use o comando python main
