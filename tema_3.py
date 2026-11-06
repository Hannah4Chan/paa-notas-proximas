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


def demonstracao_interativa():
    """Compara os algoritmos para notas digitadas, sem executar experimentos."""
    print('DEMONSTRAÇÃO INTERATIVA: as duas notas mais próximas')
    print('Digite inteiros separados por espaços ou vírgulas; sair para encerrar.')
    print('Contagens: diferenças na ingênua; comparações + diferenças na esperta.')
    while True:
        try:
            entrada = input('\nNotas: ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\nDemonstração encerrada.')
            return
        if entrada.lower() == 'sair':
            print('Demonstração encerrada.')
            return
        try:
            notas = [int(valor) for valor in entrada.replace(',', ' ').split()]
        except ValueError:
            print('Entrada inválida: use apenas inteiros separados por espaços ou vírgulas.')
            continue
        if len(notas) < 2:
            print('Informe pelo menos duas notas inteiras.')
            continue
        ingenua, diferencas = notas_proximas_ingenua(notas)
        esperta, ordenacao, varredura = notas_proximas_esperta_detalhada(notas)
        print(f'Notas informadas: {notas}')
        print(f'Ingênua: par {ingenua[:2]}; diferença mínima = {ingenua[2]}; '
              f'diferenças = {diferencas}')
        print(f'Esperta: par {esperta[:2]}; diferença mínima = {esperta[2]}; '
              f'ordenação = {ordenacao}; varredura = {varredura}; '
              f'total = {ordenacao + varredura}')
        print('Resultados coincidem: ' + ('sim' if ingenua == esperta else 'não'))


def main(argumentos=None):
    import argparse
    import unittest
    import testes_tema_3
    from experimentos_tema_3 import executar_experimentos

    parser = argparse.ArgumentParser(description='Experimentos de contagem do Tema 3')
    modos = parser.add_mutually_exclusive_group()
    modos.add_argument('--interativo', action='store_true',
                       help='Digitar notas e comparar os algoritmos, sem gerar CSV')
    modos.add_argument('--rapido', action='store_true',
                        help='Execução parcial: n=100,200 e três amostras por tamanho')
    parser.add_argument('--csv', help='Caminho alternativo para o CSV de saída')
    opcoes = parser.parse_args(argumentos)
    if opcoes.interativo:
        if opcoes.csv is not None:
            parser.error('--csv não pode ser usado com --interativo')
        demonstracao_interativa()
        return
    # A infraestrutura é testada pela suíte completa. Aqui rodam os oito testes
    # de correção; incluir o teste de subprocesso causaria recursão do comando.
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(testes_tema_3.TestesTema3)
    if not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful():
        raise SystemExit(1)
    if opcoes.rapido:
        from pathlib import Path
        print('MODO RÁPIDO: resultados parciais, não substituem o experimento completo.')
        executar_experimentos((100, 200), (), 3,
                              opcoes.csv or Path(__file__).resolve().with_name('medicoes_rapidas.csv'))
    else:
        executar_experimentos(caminho=opcoes.csv)


if __name__ == '__main__':
    main()
