"""As duas notas mais próximas: versões instrumentadas do Tema 3."""
from trabalho_base import mergesort


def notas_proximas_ingenua(notas):
    """Retorna ((menor, maior, diferença), diferenças calculadas), ou (None, 0)."""
    melhor = None
    contagem = 0
    for i in range(len(notas)):
        for j in range(i + 1, len(notas)):
            a, b = notas[i], notas[j]
            diferenca = abs(a - b)
            contagem += 1
            if a > b:
                a, b = b, a
            candidato = (a, b, diferenca)
            if (melhor is None or diferenca < melhor[2]
                    or (diferenca == melhor[2] and candidato[:2] < melhor[:2])):
                melhor = candidato
    return melhor, contagem


def notas_proximas_esperta_detalhada(notas):
    """Retorna (resultado, comparacoes_ordenacao, diferencas_varredura)."""
    ordenadas, comparacoes_ordenacao = mergesort(notas)
    melhor = None
    diferencas_varredura = 0
    for i in range(1, len(ordenadas)):
        a, b = ordenadas[i - 1], ordenadas[i]
        diferenca = b - a
        diferencas_varredura += 1
        candidato = (a, b, diferenca)
        if (melhor is None or diferenca < melhor[2]
                or (diferenca == melhor[2] and candidato[:2] < melhor[:2])):
            melhor = candidato
    return melhor, comparacoes_ordenacao, diferencas_varredura


def notas_proximas_esperta(notas):
    """Retorna (resultado, soma das contagens das duas fases), ou (None, 0)."""
    resultado, ordenacao, varredura = notas_proximas_esperta_detalhada(notas)
    return resultado, ordenacao + varredura


def main():
    import unittest
    import testes_tema_3

    suite = unittest.defaultTestLoader.loadTestsFromModule(testes_tema_3)
    if not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful():
        raise SystemExit(1)
    for notas in ([45, 70, 48, 90, 62], [10, 3, 11, 4], [9, 9, 2, 2]):
        print(f"\nEntrada: {notas}")
        print(f"Ingênua (resultado, diferenças): {notas_proximas_ingenua(notas)}")
        print(f"Esperta (resultado, total): {notas_proximas_esperta(notas)}")
        print("Esperta (resultado, ordenação, varredura):",
              notas_proximas_esperta_detalhada(notas))


if __name__ == '__main__':
    main()
