import re

def tokenizar(texto: str, modo: str='simples') -> list:
    """
    Função para tokenizar um texto usando expressão regular.
    
    Parâmetros:
    - texto (str): o texto a ser tokenizado
    - modo (str): 'simples', 'pontuacao' ou 'avancado'
    
    Retorno:
    - lista de tokens
    """
    if modo == 'simples':
        padrao = r'\w+'
    elif modo == 'pontuacao':
        padrao = r'\w+|[^\w\s]'
    elif modo == 'avancado':
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
print(tokenizar(texto_exemplo, modo='simples'))
print("=================================")

print("=== Tokenização com Pontuação ===")
print(tokenizar(texto_exemplo, modo='pontuacao'))
print("=================================")

print("=== Tokenização Avançada (tratando contrações) ===")
print(tokenizar(texto_exemplo, modo='avancado'))
print()
