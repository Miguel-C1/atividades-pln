import torch
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
import time
import re


def carregar_modelo():
    """
    Carrega o modelo e o tokenizer mBART pré-treinados.
    Esta função deve ser chamada apenas uma vez.
    """
    print("Iniciando o carregamento do modelo mBART-large-50...")
    print("Isso pode levar alguns minutos e consumir >2GB de RAM.")
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Usando dispositivo: {device}")

    modelo = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt").to(device)
    tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
    
    tokenizer.src_lang = "pt_XX"
    tokenizer.tgt_lang = "pt_XX"
    
    print("Modelo carregado com sucesso!")
    return modelo, tokenizer, device

def preprocessar_texto(texto: str) -> str:
    """
    Realiza uma limpeza e normalização básica no texto de entrada.
    """
    texto = texto.replace('\t', ' ')
    texto = re.sub(r'\n+', '\n', texto) 
    texto = texto.replace('‑', '-') 
    texto = texto.replace(' ', ' ') 
    texto = re.sub(r'\s{2,}', ' ', texto)
    texto = re.sub(r'https?://\S+|www\.\S+', '', texto)
    texto = re.sub(r'<.*?>', '', texto)
    texto = texto.strip()
    
    return texto

def resumir(modelo, tokenizer, device, texto: str, max_length: int = 400, min_length: int = 50, num_beams: int = 5):
    """
    Gera um resumo abstrativo do texto fornecido.
    
    Args:
        modelo: O modelo mBART carregado.
        tokenizer: O tokenizer mBART carregado.
        device: O dispositivo (CPU ou CUDA) onde o modelo está.
        texto: O texto em português a ser resumido.
        max_length: O comprimento máximo do resumo gerado.
        min_length: O comprimento mínimo do resumo gerado.
        num_beams: O número de "feixes" para o beam search (melhora a qualidade).
    """

    inputs = tokenizer(texto, return_tensors="pt", max_length=2048, truncation=True).to(device)
    
    summary_ids = modelo.generate(
        inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        num_beams=num_beams,
        max_length=max_length,
        min_length=min_length,
        forced_bos_token_id=tokenizer.lang_code_to_id["pt_XX"],
        early_stopping=True
    )
    
    resumo = tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)[0]
    return resumo

if __name__ == "__main__":
    start_time = time.time()
    modelo, tokenizer, device = carregar_modelo()
    end_time = time.time()
    print(f"Tempo de carregamento do modelo: {end_time - start_time:.2f} segundos.\n")

    try:
        with open("texto_original.txt", "r", encoding="utf-8") as f:
            texto_original = f.read()
    except FileNotFoundError:
        print("Erro: Arquivo 'texto_original.txt' não encontrado.")
        print("Crie o arquivo e insira o texto a ser resumido.")
        exit()

    print("Aplicando pré-processamento de limpeza no texto...")
    texto_original_processado = preprocessar_texto(texto_original)
    print("Pré-processamento concluído.\n")

    print("Iniciando o processo de sumarização...")
    start_time = time.time()
    resumo_gerado = resumir(modelo, tokenizer, device, texto_original_processado)
    end_time = time.time()
    print(f"Tempo de sumarização: {end_time - start_time:.2f} segundos.\n")

    palavras_original = len(texto_original_processado.split())
    palavras_resumo = len(resumo_gerado.split())
    
    print("="*20 + " TEXTO ORIGINAL " + "="*20)
    print(texto_original_processado)
    print(f"\n(Contagem de palavras: {palavras_original})\n")
    
    print("="*20 + " RESUMO ABSTRATIVO GERADO " + "="*20)
    print(resumo_gerado)
    print(f"\n(Contagem de palavras: {palavras_resumo})\n")

    print("="*20 + " ANÁLISE " + "="*20)
    reducao = 100 - (palavras_resumo / palavras_original * 100)
    print(f"O resumo é {reducao:.2f}% menor que o texto original.")
    if palavras_resumo <= palavras_original / 2:
        print("Critério da tarefa (resumo <= 50% do original) foi ATENDIDO.")
    else:
        print("Critério da tarefa (resumo <= 50% do original) NÃO foi atendido.")