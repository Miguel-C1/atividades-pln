import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
import re

def carregar_modelo(model_name="unicamp-dl/ptt5-base-portuguese-vocab"):
    """
    Carrega o modelo e o tokenizer T5 em português.
    Usa GPU se disponível.
    """
    print("Carregando modelo e tokenizador...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Dispositivo em uso: {device}")

    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name).to(device)

    print("Modelo carregado com sucesso!")
    return model, tokenizer, device

def preprocessar_texto(texto: str) -> str:
    """
    Limpa o texto de entrada para melhorar a qualidade da sumarização.
    """
    texto = texto.replace('\t', ' ')
    texto = re.sub(r'\n+', '\n', texto)
    texto = texto.replace('‑', '-')
    texto = texto.replace(' ', ' ')
    texto = re.sub(r'\s{2,}', ' ', texto)
    texto = re.sub(r'https?://\S+|www\.\S+', '', texto)
    texto = re.sub(r'<.*?>', '', texto)
    return texto.strip()

def resumir(texto: str, model, tokenizer, device, max_length=400, min_length=40, num_beams=4):
    """
    Gera um resumo abstrativo do texto fornecido usando T5.
    """
    prefixo_tarefa = "sumarize: "
    entrada = prefixo_tarefa + preprocessar_texto(texto)

    inputs = tokenizer(
        entrada,
        return_tensors="pt",
        max_length=1024,
        truncation=True
    ).to(device)

    summary_ids = model.generate(
        inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_length=max_length,
        min_length=min_length,
        num_beams=num_beams,
        early_stopping=True
    )

    resumo = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return resumo

def gerar_estatisticas_simples(texto_original: str, texto_resumido: str):
    """
    Calcula e imprime a contagem de palavras e a taxa de compressão.
    """
    palavras_orig = len(re.findall(r'\b\w+\b', texto_original))
    palavras_resumo = len(re.findall(r'\b\w+\b', texto_resumido))

    if palavras_orig > 0:
        taxa_compressao = (1 - (palavras_resumo / palavras_orig)) * 100
    else:
        taxa_compressao = 0

    print("\n--- ESTATÍSTICAS DE SUMARIZAÇÃO ---")
    print(f"Palavras no texto original: {palavras_orig}")
    print(f"Palavras no resumo: {palavras_resumo}")
    print(f"Taxa de compressão (redução de palavras): {taxa_compressao:.2f}%")

if __name__ == "__main__":
    try:
        with open("texto_original.txt", "r", encoding="utf-8") as f:
            texto_original = f.read()
    except FileNotFoundError:
        print("Erro: Arquivo 'texto_original.txt' não encontrado.")
        print("Crie o arquivo e insira o texto a ser resumido.")
        exit()

    
    model, tokenizer, device = carregar_modelo()
    resumo = resumir(texto_original, model, tokenizer, device)
    print("\n--- RESUMO GERADO ---")
    print(resumo)
    gerar_estatisticas_simples(texto_original, resumo)