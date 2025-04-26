import re

def tokenizar(texto: str, modo: int=1) -> list:
    """
    Função para tokenizar um texto usando expressão regular.
    
    Parâmetros:
    - texto (str): o texto a ser tokenizado
    - modo (str): 'simples', 'pontuacao' ou 'avancado'
    
    Retorno:
    - lista de tokens
    """
    if modo == 1:
        padrao = r'\w+'
    elif modo == 2:
        padrao = r'\w+|[^\w\s]'
    elif modo == 3:
        # Palavras considerando contrações, sinais separados
        padrao = r'\w+(?:[’\']\w+)?|[^\w\s]'
    else:
        raise ValueError(f"Modo '{modo}' não reconhecido. Use 'simples', 'pontuacao' ou 'avancado'.")
    
    tokens = re.findall(padrao, texto, flags=re.UNICODE)
    return tokens

texto_exemplo = "Olá, tudo bem? 432 22 1 Vamos tokenizar este texto! Eu não tô brincando. Pegue um copo d'água e venha aqui."

print("=== Texto original ===")
print(texto_exemplo)

print("=== Tokenização Simples ===")
print(tokenizar(texto_exemplo, modo=1))
print("=================================")

print("=== Tokenização com Pontuação ===")
print(tokenizar(texto_exemplo, modo=2))
print("=================================")

print("=== Tokenização Avançada (tratando contrações) ===")
print(tokenizar(texto_exemplo, modo=3))
print()
