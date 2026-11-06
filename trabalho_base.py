"""trabalho_base.py — Base comum do Trabalho Prático
Contagem de Operações: Lineares, Quadráticos e Logarítmicos
Projeto e Análise de Algoritmos — CIESA — 4º/6º período
Use este arquivo em todas as equipes: ele garante que as tabelas sejam comparáveis entre si.
Importe o que precisar no arquivo do seu tema:
    from trabalho_base import mergesort, busca_binaria, teste_do_dobro, aleatorio
Convenção: toda função instrumentada devolve (resultado, contagem).
Rode este arquivo sozinho para ver as "assinaturas" de duas classes:
    python trabalho_base.py
"""
import csv
import math
import random
import sys

sys.setrecursionlimit(10_000)


# =================================================================
# Ordenação instrumentada (mergesort da Aula 04)
# =================================================================
def mergesort(v):
    """Devolve (nova lista ordenada, comparações). Não altera v. Estável."""
    if len(v) <= 1:
        return list(v), 0
    meio = len(v) // 2
    esquerda, c1 = mergesort(v[:meio])
    direita, c2 = mergesort(v[meio:])
    resultado = []
    i = j = 0
    comps = c1 + c2
    while i < len(esquerda) and j < len(direita):
        comps += 1  # esquerda[i] <= direita[j]
        if esquerda[i] <= direita[j]:
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1
    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])
    return resultado, comps


# =================================================================
# Busca binária instrumentada (Aula 03)
# =================================================================
def busca_binaria(lista, alvo):
    """lista em ordem crescente. Devolve (posição ou -1, voltas do while).
    Funciona também com range(n), que não ocupa memória.
    """
    lo, hi = 0, len(lista) - 1
    voltas = 0
    while lo <= hi:
        voltas += 1
        meio = (lo + hi) // 2
        if lista[meio] == alvo:
            return meio, voltas
        if lista[meio] < alvo:
            lo = meio + 1
        else:
            hi = meio - 1
    return -1, voltas


# =================================================================
# Geradores de entrada (sempre com semente registrada)
# =================================================================
def aleatorio(n, lo=0, hi=100, semente=42):
    """n inteiros aleatórios entre lo e hi (inclusive). Pode haver repetidos."""
    gerador = random.Random(semente)
    return [gerador.randint(lo, hi) for _ in range(n)]


def distintos(n, semente=42):
    """Permutação aleatória de 0..n-1: todos os valores diferentes."""
    gerador = random.Random(semente)
    v = list(range(n))
    gerador.shuffle(v)
    return v


def ordenado(n):
    return list(range(n))


def invertido(n):
    return list(range(n, 0, -1))


def matriculas(n, semente=42, repetidas=0):
    """n matrículas distintas no formato AAAASNNNNN (ex.: 2026200137), n até 99 999.
    repetidas = quantas posições recebem cópia de outra matrícula.
    """
    gerador = random.Random(semente)
    base = gerador.sample(range(1, 100_000), n)
    v = [int(f"20262{x:05d}") for x in base]
    for _ in range(repetidas):
        i, j = gerador.randrange(n), gerador.randrange(n)
        v[i] = v[j]
    return v


# =================================================================
# Teste do dobro e dados brutos
# =================================================================
def _num(x):
    return f"{x:.2f}" if isinstance(x, float) and not x.is_integer() else str(int(x))


def teste_do_dobro(titulo, contagem, tamanhos=(100, 200, 400, 800, 1600), versao="",
                   dados=None):
    """contagem(n) devolve o número de operações para uma entrada de tamanho n.
    Imprime c, as razões e a coluna 'dobro' = c(n) / c(n/2).
    A classe do algoritmo é a da razão que ESTABILIZA.
    Se 'dados' for uma lista, acrescenta nela as linhas para o CSV.
    """
    print(f"\n{titulo}")
    print(f"{'n':>8} {'c':>11} {'c/log2n':>9} {'c/n':>9} {'c/nlog2n':>9} "
          f"{'c/n²':>9} {'c/n³':>10} {'dobro':>6}")
    anterior = None
    for n in tamanhos:
        c = contagem(n)
        lg = math.log2(n)
        dobro = f"{c / anterior:.2f}" if anterior else "-"
        print(f"{n:>8} {_num(c):>11} {c / lg:>9.2f} {c / n:>9.3f} {c / (n * lg):>9.3f} "
              f"{c / n**2:>9.4f} {c / n**3:>10.6f} {dobro:>6}")
        if dados is not None:
            dados.append({"versao": versao or titulo, "n": n, "contagem": c})
        anterior = c


def salvar_csv(dados, caminho="medicoes.csv"):
    """Grava as linhas acumuladas pelo teste_do_dobro (dados brutos)."""
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=["versao", "n", "contagem"])
        escritor.writeheader()
        escritor.writerows(dados)
    print(f"\n{len(dados)} linhas gravadas em {caminho}")


# =================================================================
# Demonstração: as assinaturas de n log n e de log n
# =================================================================
if __name__ == "__main__":
    v = [5, 2, 9, 1, 5, 6]
    assert mergesort(v)[0] == sorted(v) and v == [5, 2, 9, 1, 5, 6]
    assert busca_binaria(range(1_000_000), 765_432)[0] == 765_432
    assert busca_binaria([1, 3, 5], 4)[0] == -1
    dados = []
    teste_do_dobro("Mergesort em entrada aleatória (comparações)",
                   lambda n: mergesort(distintos(n))[1], versao="mergesort", dados=dados)
    teste_do_dobro("Uma busca binária, pior caso (voltas)",
                   lambda n: busca_binaria(range(n), n)[1], versao="busca_binaria", dados=dados)
    salvar_csv(dados, "medicoes_exemplo.csv")
