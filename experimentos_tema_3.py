"""Experimentos reproduzíveis do Tema 3, sem alterar os algoritmos medidos."""
from pathlib import Path
from trabalho_base import aleatorio, salvar_csv, teste_do_dobro

TAMANHOS = (100, 200, 400, 800, 1600)
TAMANHOS_AMPLIADOS = (12500, 25000, 50000, 100000)
REPETICOES = 30


def melhor_caso(n):
    """Notas iguais esgotam a metade esquerda em cada intercalação."""
    return [0] * n


def pior_caso(n):
    """Permutação de 0..n-1 que força n-1 comparações em cada intercalação."""
    def construir(valores):
        if len(valores) <= 1:
            return valores
        # Metade esquerda com floor(n/2) valores, direita com ceil(n/2).
        # Depois de ordenadas, elas se alternam até a penúltima comparação.
        return construir(valores[1::2]) + construir(valores[::2])
    return construir(list(range(n)))


def comparacoes_extremas(n):
    """Recorrências B(n)=B(a)+B(b)+a; W(n)=W(a)+W(b)+n-1."""
    if n <= 1:
        return 0, 0
    a = n // 2
    b = n - a
    melhor_a, pior_a = comparacoes_extremas(a)
    melhor_b, pior_b = comparacoes_extremas(b)
    return melhor_a + melhor_b + a, pior_a + pior_b + n - 1


def semente_media(n, repeticao):
    """Sementes distintas por tamanho e repetição (índice iniciado em zero)."""
    return 202600000 + n * 100 + repeticao


def entrada_media(n, repeticao):
    """Amostra de inteiros uniformes independentes de 0 a 100, com reposição."""
    return aleatorio(n, 0, 100, semente=semente_media(n, repeticao))


def medir(notas, incluir_ingenua):
    """Mede uma mesma entrada nas versões aplicáveis e confere os contadores."""
    from tema_3 import notas_proximas_ingenua, notas_proximas_esperta_detalhada
    n = len(notas)
    resultado, ordenacao, varredura = notas_proximas_esperta_detalhada(notas)
    if varredura != (n - 1 if n >= 2 else 0):
        raise AssertionError('Contador de varredura inconsistente')
    fases = [('esperta', 'ordenacao', ordenacao),
             ('esperta', 'varredura', varredura),
             ('esperta', 'total', ordenacao + varredura)]
    if incluir_ingenua:
        ingenua, diferencas = notas_proximas_ingenua(notas)
        if ingenua != resultado or diferencas != n * (n - 1) // 2:
            raise AssertionError('Resultado ou contador da versão ingênua inconsistente')
        fases.append(('ingenua', 'diferencas', diferencas))
    return fases


def executar_experimentos(tamanhos=TAMANHOS, ampliados=TAMANHOS_AMPLIADOS,
                          repeticoes=REPETICOES, caminho=None):
    """Mede, imprime tabelas pela base e salva amostras e resumos no CSV.

    Parâmetros reduzidos são usados apenas nos testes e no modo rápido.
    As tabelas recebem contagens já medidas; não executam os algoritmos de novo.
    """
    if repeticoes < 1:
        raise ValueError('É necessária pelo menos uma repetição')
    if caminho is None:
        caminho = Path(__file__).resolve().with_name('medicoes.csv')
    dados = []
    resumos = {}
    print('Caso médio: inteiros uniformes independentes de 0 a 100, com reposição.')
    print(f'Repetições por tamanho: {repeticoes}; semente = 202600000 + 100*n + r; r começa em 0.')
    print('Melhor caso: todas as notas zero. Pior caso: permutação de 0..n-1, série distinta.')
    for cenario in ('melhor', 'pior_distintos', 'medio'):
        for n in tuple(tamanhos) + tuple(ampliados):
            somas = {}
            quantidade = repeticoes if cenario == 'medio' else 1
            for r in range(quantidade):
                if cenario == 'melhor':
                    notas = melhor_caso(n)
                elif cenario == 'pior_distintos':
                    notas = pior_caso(n)
                else:
                    notas = entrada_media(n, r)
                fases = medir(notas, n in tamanhos)
                if cenario != 'medio':
                    esperado = comparacoes_extremas(n)[0 if cenario == 'melhor' else 1]
                    if fases[0][2] != esperado:
                        raise AssertionError('Construção extrema diverge da recorrência')
                for versao, fase, contagem in fases:
                    chave = (versao, cenario, fase, n)
                    somas[chave] = somas.get(chave, 0) + contagem
                    if cenario == 'medio':
                        identificador = (f'{versao}/{cenario}/{fase}/rep={r:02d}'
                                         f'/semente={semente_media(n, r)}')
                        dados.append({'versao': identificador, 'n': n, 'contagem': contagem})
            for chave, soma in somas.items():
                resumos[chave] = soma / quantidade if cenario == 'medio' else soma

    # Séries separadas: o salto 1600 -> 12500 nunca vira uma razão de dobro.
    for cenario in ('melhor', 'pior_distintos', 'medio'):
        for versao, fases, series in (
            ('ingenua', ('diferencas',), (('padrao', tamanhos),)),
            ('esperta', ('ordenacao', 'varredura', 'total'),
             (('padrao', tamanhos), ('ampliada', ampliados)))):
            for serie, ns in series:
                if not ns:
                    continue
                for fase in fases:
                    identificador = f'{versao}/{cenario}/{fase}'
                    if cenario == 'medio':
                        identificador += '/media'
                    teste_do_dobro(
                        f'{identificador} | serie {serie}',
                        lambda n, v=versao, c=cenario, f=fase: resumos[(v, c, f, n)],
                        tamanhos=ns, versao=identificador, dados=dados)
    salvar_csv(dados, caminho)
    return dados
