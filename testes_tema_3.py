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


class TestesExperimentos(unittest.TestCase):
    def test_extremos_mergesort(self):
        from experimentos_tema_3 import melhor_caso, pior_caso, comparacoes_extremas
        for n in range(7):
            contagens = [mergesort(p)[1] for p in itertools.permutations(range(n))]
            self.assertEqual(mergesort(melhor_caso(n))[1], min(contagens))
            self.assertEqual(mergesort(pior_caso(n))[1], max(contagens))
            self.assertEqual(sorted(pior_caso(n)), list(range(n)))
        for n in (7, 9, 17, 100, 200, 400, 800, 1600):
            self.assertEqual(mergesort(melhor_caso(n))[1], comparacoes_extremas(n)[0])
            self.assertEqual(mergesort(pior_caso(n))[1], comparacoes_extremas(n)[1])
            altura = (n - 1).bit_length()
            self.assertEqual(comparacoes_extremas(n)[1], n * altura - 2**altura + 1)

    def test_sementes_reproduziveis(self):
        from experimentos_tema_3 import entrada_media, semente_media
        sementes = [semente_media(100, r) for r in range(30)]
        self.assertEqual(len(set(sementes)), 30)
        entradas = [entrada_media(100, r) for r in range(30)]
        self.assertEqual(len({tuple(v) for v in entradas}), 30)
        self.assertEqual(entrada_media(100, 7), entrada_media(100, 7))
        self.assertEqual(entrada_media(100, 7), aleatorio(100, 0, 100, sementes[7]))

    def test_medicao_media_tabelas_csv(self):
        import contextlib
        import csv
        import io
        import tempfile
        from pathlib import Path
        from experimentos_tema_3 import executar_experimentos, entrada_media
        saida = io.StringIO()
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as pasta, contextlib.redirect_stdout(saida):
            caminho = Path(pasta) / 'medicoes.csv'
            from unittest.mock import patch
            from trabalho_base import teste_do_dobro
            with patch('experimentos_tema_3.teste_do_dobro', wraps=teste_do_dobro) as tabelas:
                dados = executar_experimentos((4, 8), (16,), 3, caminho)
            self.assertEqual(tabelas.call_count, 21)
            for chamada in tabelas.call_args_list:
                for n in chamada.kwargs['tamanhos']:
                    valor_tabela = chamada.args[1](n)
                    valor_csv = next(d['contagem'] for d in dados
                                     if d['n'] == n and d['versao'] == chamada.kwargs['versao'])
                    self.assertEqual(valor_tabela, valor_csv)
            with caminho.open(encoding='utf-8', newline='') as f:
                leitor = csv.DictReader(f)
                self.assertEqual(leitor.fieldnames, ['versao', 'n', 'contagem'])
                linhas = list(leitor)
            self.assertEqual(len(linhas), len(dados))
            self.assertEqual(len({(d['versao'], d['n']) for d in dados}), len(dados))
            for linha, dado in zip(linhas, dados):
                self.assertEqual(linha['versao'], dado['versao'])
                self.assertEqual(int(linha['n']), dado['n'])
                self.assertEqual(float(linha['contagem']), dado['contagem'])
            for n in (4, 8, 16):
                contagens = [notas_proximas_esperta_detalhada(entrada_media(n, r))
                             for r in range(3)]
                for fase, valores in (
                    ('ordenacao', [c[1] for c in contagens]),
                    ('varredura', [c[2] for c in contagens]),
                    ('total', [c[1] + c[2] for c in contagens])):
                    individuais = [d['contagem'] for d in dados
                                    if d['n'] == n and d['versao'].startswith(
                                        'esperta/medio/' + fase + '/rep=')]
                    self.assertEqual(individuais, valores)
                    media = next(d['contagem'] for d in dados
                                 if d['n'] == n and d['versao'] ==
                                 'esperta/medio/' + fase + '/media')
                    self.assertEqual(media, sum(individuais) / 3)
                for d in dados:
                    if d['n'] == n and d['versao'].startswith('ingenua/'):
                        self.assertNotEqual(n, 16)
                        self.assertEqual(d['contagem'], n * (n - 1) // 2)
            # A tabela da base apresenta a média com duas casas, sem mudar o CSV.
            media4 = sum(c[1] for c in [notas_proximas_esperta_detalhada(
                entrada_media(4, r)) for r in range(3)]) / 3
            self.assertIn(f'{media4:.2f}', saida.getvalue())
            self.assertIn('dobro', saida.getvalue())

    def test_comando_principal_rapido(self):
        import subprocess
        import sys
        import tempfile
        from pathlib import Path
        script = Path(__file__).resolve().with_name('tema_3.py')
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as pasta:
            processo = subprocess.run(
                [sys.executable, '-X', 'utf8', str(script), '--rapido',
                 '--csv', str(Path(pasta) / 'rapido.csv')],
                cwd=pasta, capture_output=True, text=True, encoding='utf-8',
                timeout=60)
            self.assertEqual(processo.returncode, 0, processo.stderr)
            self.assertIn('MODO RÁPIDO', processo.stdout)
            self.assertIn('OK', processo.stderr)
            self.assertTrue((Path(pasta) / 'rapido.csv').exists())
        # O modo rápido usa o mesmo medidor; não deve substituir o CSV completo.

    def test_interrompe_se_testes_falham(self):
        from unittest.mock import patch
        import tema_3
        with patch('unittest.TextTestRunner.run') as executar:
            executar.return_value.wasSuccessful.return_value = False
            with patch('experimentos_tema_3.executar_experimentos') as medir:
                with self.assertRaises(SystemExit):
                    tema_3.main([])
                medir.assert_not_called()


if __name__ == '__main__':
    unittest.main()
