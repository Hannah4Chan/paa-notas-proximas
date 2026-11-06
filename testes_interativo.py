"""Testes do comando interativo, sem modificar os CSVs do projeto."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class TestesInterativo(unittest.TestCase):
    def executar(self, entrada, *opcoes):
        script = Path(__file__).resolve().with_name('tema_3.py')
        with tempfile.TemporaryDirectory() as pasta:
            processo = subprocess.run(
                [sys.executable, '-X', 'utf8', str(script), '--interativo', *opcoes],
                input=entrada, capture_output=True, text=True, encoding='utf-8',
                cwd=pasta, timeout=10)
            self.assertEqual(list(Path(pasta).iterdir()), [])
        return processo

    def test_resultado_contagens_e_repeticao(self):
        p = self.executar('4 1 3 2\n9, 9, 2, 2\nsair\n')
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn('Ingênua: par (1, 2); diferença mínima = 1; diferenças = 6', p.stdout)
        self.assertIn('Esperta: par (1, 2); diferença mínima = 1', p.stdout)
        self.assertIn('ordenação = 5; varredura = 3; total = 8', p.stdout)
        self.assertIn('par (2, 2); diferença mínima = 0', p.stdout)
        self.assertEqual(p.stdout.count('Resultados coincidem: sim'), 2)

    def test_validacao_e_desempate(self):
        p = self.executar('\n7\n1 a\n1.5 2\n10 3 11 4\n-9 -3 -8 10\n')
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(p.stdout.count('Informe pelo menos duas notas inteiras.'), 2)
        self.assertEqual(p.stdout.count('Entrada inválida: use apenas inteiros'), 2)
        self.assertIn('par (3, 4); diferença mínima = 1', p.stdout)
        self.assertIn('par (-9, -8); diferença mínima = 1', p.stdout)

    def test_opcoes_incompativeis(self):
        for opcoes in (('--rapido',), ('--csv', 'saida.csv')):
            with self.subTest(opcoes=opcoes):
                p = self.executar('', *opcoes)
                self.assertEqual(p.returncode, 2)


if __name__ == '__main__':
    unittest.main()
