"""Testes de correção e instrumentação do Tema 3."""
import itertools
import unittest
from trabalho_base import aleatorio, distintos, mergesort
from tema_3 import notas_proximas_ingenua, notas_proximas_esperta, notas_proximas_esperta_detalhada


def oraculo(notas):
    """Enumera pares e escolhe por (diferença, menor nota, maior nota)."""
    candidatos = [(abs(a - b), min(a, b), max(a, b))
                  for a, b in itertools.combinations(notas, 2)]
    if not candidatos:
        return None
    diferenca, a, b = min(candidatos)
    return a, b, diferenca


def entradas_aleatorias():
    """1.000 casos reproduzíveis: sementes 1000..1999, quatro grupos de 250."""
    for semente in range(1000, 2000):
        n = 2 + semente % 79
        grupo = (semente - 1000) // 250
        if grupo == 0:
            notas = aleatorio(n, 0, 100, semente=semente)
        elif grupo == 1:
            notas = aleatorio(n, 0, 1000, semente=semente)
        elif grupo == 2:
            notas = aleatorio(n, -10000, 10000, semente=semente)
        else:
            # Valores distintos com deslocamento e espaçamento variados.
            deslocamento, sorteio = aleatorio(2, -500, 500, semente=semente)
            passo = 2 + abs(sorteio) % 19
            notas = [deslocamento + passo * x
                     for x in distintos(n, semente=semente)]
        yield semente, grupo, notas


class TestesTema3(unittest.TestCase):
    def verificar(self, notas, esperado=None):
        original = notas[:]
        referencia = oraculo(notas) if esperado is None else esperado
        ingenua, pares = notas_proximas_ingenua(notas)
        self.assertEqual(notas, original)
        esperta, total = notas_proximas_esperta(notas)
        self.assertEqual(notas, original)
        detalhado, ordenacao, varredura = notas_proximas_esperta_detalhada(notas)
        self.assertEqual(notas, original)
        self.assertEqual(ingenua, referencia)
        self.assertEqual(esperta, referencia)
        self.assertEqual(detalhado, referencia)
        n = len(notas)
        self.assertEqual(pares, n * (n - 1) // 2)
        self.assertEqual(varredura, n - 1 if n >= 2 else 0)
        self.assertEqual(ordenacao, mergesort(notas)[1])
        self.assertEqual(total, ordenacao + varredura)

    def test_bordas_e_exemplos(self):
        casos = [[], [8], [9, 2], [45, 70, 48, 90, 62],
                 [1, 3, 5, 8], [8, 5, 3, 1], [7] * 12,
                 [8, 4, 8, 2, 4], [10, 3, 11, 4],
                 [9, 9, 2, 2], [-9, -3, -8, 10]]
        for notas in casos:
            with self.subTest(notas=notas):
                self.verificar(notas)

    def test_desempate_obrigatorio(self):
        self.verificar([10, 3, 11, 4], (3, 4, 1))

    def test_contratos_sem_par(self):
        for notas in ([], [42]):
            self.assertEqual(notas_proximas_ingenua(notas), (None, 0))
            self.assertEqual(notas_proximas_esperta(notas), (None, 0))
            self.assertEqual(notas_proximas_esperta_detalhada(notas), (None, 0, 0))

    def test_exaustivo_pequeno(self):
        for n in range(6):
            for valores in itertools.product((-1, 0, 1), repeat=n):
                self.verificar(list(valores))

    def test_mil_entradas_aleatorias(self):
        listas = set()
        resultados = set()
        zeros = positivos = empates = quantidade = 0
        for semente, grupo, notas in entradas_aleatorias():
            with self.subTest(semente=semente, grupo=grupo):
                self.verificar(notas)
            quantidade += 1
            listas.add(tuple(notas))
            resultado = oraculo(notas)
            resultados.add(resultado)
            diferenca = resultado[2]
            zeros += diferenca == 0
            positivos += diferenca > 0
            pares_minimos = {tuple(sorted((a, b)))
                             for a, b in itertools.combinations(notas, 2)
                             if abs(a - b) == diferenca}
            empates += len(pares_minimos) > 1
        self.assertEqual(quantidade, 1000)
        self.assertGreater(len(listas), 1)
        self.assertGreater(len(resultados), 1)
        self.assertGreater(zeros, 0)
        self.assertGreater(positivos, 0)
        self.assertGreater(empates, 0)

    def test_contadores_por_tamanho_e_ordem(self):
        for n in (0, 1, 2, 3, 8, 17, 100, 200):
            for notas in (list(range(n)), list(range(n, 0, -1)), [5] * n):
                self.verificar(notas)

    def test_contagens_conhecidas(self):
        self.assertEqual(notas_proximas_ingenua([4, 1, 3, 2])[1], 6)
        self.assertEqual(notas_proximas_esperta_detalhada([4, 1, 3, 2]),
                         ((1, 2, 1), 5, 3))

    def test_entrada_maior(self):
        self.verificar(aleatorio(1600, semente=2026))


if __name__ == '__main__':
    unittest.main()
