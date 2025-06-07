# Modelo Bag-of-Words: Impacto do Pré-Processamento

## Visão Geral
Sem um pré-processamento adequado, um modelo Bag-of-Words (BoW) sofre de **explosão de dimensionalidade** e **redundância** de tokens: palavras semanticamente idênticas ou variações morfológicas aparecem como atributos distintos, tornando o vetor muito esparso e prejudicando tanto a performance quanto a capacidade de generalização do modelo.

---

## 1. Sem pré-processamento

**Tokenização bruta**
- Mantém maiúsculas/minúsculas distintas: “Eu” ≠ “eu”
- Preserva pontuação junto às palavras: “água!” ≠ “água”
- Não trata variações morfológicas (“quero” ≠ “queria” ≠ “preferiria”)

**Léxico e cardinalidade**  
```
Lexico bruto (|V| = 12):
["Eu", "quero", "tomar", "água!", "eu,", "prefiro", "café.",
 "preferiria", "café", "quente.", "queria", "água?"]
Dimensão do vetor: 12
```

**Vetores BoW brutos**

| Frase ↓ \ Token → | Eu | quero | tomar | água! | eu, | prefiro | café. | preferiria | café | quente. | queria | água? |
|-------------------|:--:|:-----:|:-----:|:-----:|:---:|:-------:|:-----:|:----------:|:----:|:--------:|:------:|:------:|
| **F1: “Eu quero tomar água!”**         | 1  |   1   |   1   |   1   |  0  |    0    |   0   |     0      |  0   |    0     |   0    |   0    |
| **F2: “eu, prefiro tomar café.”**      | 0  |   0   |   1   |   0   |  1  |    1    |   1   |     0      |  0   |    0     |   0    |   0    |
| **F3: “Eu preferiria tomar café quente.”** | 1  |   0   |   1   |   0   |  0  |    0    |   0   |     1      |  1   |    1     |   0    |   0    |
| **F4: “Eu queria tomar água?”**        | 1  |   0   |   1   |   0   |  0  |    0    |   0   |     0      |  0   |    0     |   1    |   1    |

---

## 2. Com pré-processamento (remoção de pontuação, lowercasing, lematização)

**Transformações aplicadas**
- Converter tudo para minúsculas
- Remover caracteres especiais e pontuação
- Lematizar/stemizar (“quero”→“querer”, “queria”→“querer”, “prefiro”/“preferiria”→“preferir”, “café”→“cafe”, “água”→“agua”)

**Novo léxico e cardinalidade**  
```
Léxico processado (|V′| = 7):
["eu", "querer", "tomar", "agua", "preferir", "cafe", "quente"]
Dimensão do vetor: 7
```

**Vetores BoW processados**

| Frase ↓ \ Token →                | eu | querer | tomar | agua | preferir | cafe | quente |
|----------------------------------|:--:|:------:|:-----:|:----:|:--------:|:----:|:------:|
| **F1: “eu quero tomar água”**         | 1  |   1    |   1   |  1   |    0     |  0   |   0    |
| **F2: “eu prefiro tomar cafe”**       | 1  |   0    |   1   |  0   |    1     |  1   |   0    |
| **F3: “eu preferir tomar cafe quente”** | 1  |   0    |   1   |  0   |    1     |  1   |   1    |
| **F4: “eu querer tomar agua”**        | 1  |   1    |   1   |  1   |    0     |  0   |   0    |

---

## 3. Impacto na cardinalidade e esparsidade

| Condição                     | Tamanho do léxico | Dimensão BoW | Exemplo de sparsidade       |
|------------------------------|:-----------------:|:------------:|:---------------------------:|
| **Sem pré-processamento**    | 12                | 12           | 75% zeros no vetor médio    |
| **Com pré-processamento**    | 7                 | 7            | ~43% zeros no vetor médio   |

**Conclusão:**  
- **Sem** remoção de pontuação e lematização, o léxico “explode” com tokens redundantes e morfemas distintos.  
- **Com** um pipeline de pré-processamento, reduz-se drasticamente a dimensionalidade, melhora-se a densidade dos vetores e preserva-se melhor a informação semântica.
