# As duas notas mais próximas

Trabalho da disciplina **Projeto e Análise de Algoritmos**, do curso de **Ciência da Computação** do **Centro Universitário de Ensino Superior do Amazonas (CIESA)**.

**Integrantes:** Hannah Veiga, Alessandro Ramos, Ednaldo Maciel e Lucas Cerquinho.  
**Professor:** Brendo.  
**Tema 3:** As duas notas mais próximas.

O objetivo é encontrar, em uma lista de notas inteiras, os dois valores com a menor diferença absoluta. Implementamos duas soluções em Python, contamos suas operações e comparamos os resultados teóricos com experimentos. O projeto também inclui testes automatizados, um modo interativo para demonstração e duas funções misteriosas preparadas para a atividade de troca entre grupos.

## Como executar

É necessário ter **Python 3** instalado. O projeto usa apenas a biblioteca padrão, sem dependências externas.

Abra o terminal na pasta onde você salvou ou clonou o projeto. No computador em que ele foi desenvolvido, o caminho é:

```powershell
cd "C:\projetos\paa-notas-proximas"
```

Se estiver em outro computador, use o caminho correspondente. Caso o comando `python` não funcione no Windows, tente `py`.

### Demonstração interativa

```powershell
python tema_3.py --interativo
```

Digite duas ou mais notas inteiras, separadas por espaços ou vírgulas. Por exemplo:

```text
4 1 3 2
```

O programa apresenta o par mais próximo, a diferença mínima e as contagens de cada algoritmo:

```text
Ingênua: par (1, 2); diferença mínima = 1; diferenças = 6
Esperta: par (1, 2); diferença mínima = 1; ordenação = 5; varredura = 3; total = 8
Resultados coincidem: sim
```

É possível testar várias listas na mesma sessão. Digite **`sair`** para encerrar. Valores negativos e repetidos são aceitos; notas decimais não são aceitas. O modo interativo não gera CSV nem executa os experimentos.

### Experimentos e testes

| Comando | O que faz |
| --- | --- |
| `python tema_3.py --rapido` | Demonstração curta com 100 e 200 elementos e três amostras por tamanho. Gera `medicoes_rapidas.csv`. |
| `python tema_3.py` | Executa os testes de correção, os experimentos completos e o teste do dobro. Atualiza `medicoes.csv`. |
| `python -m unittest testes_tema_3 testes_interativo -v` | Executa os **16 testes automatizados** do projeto. |
| `python tema_3.py --help` | Mostra as opções disponíveis. |
| `python trabalho_base.py` | Executa os exemplos e verificações da base fornecida na disciplina. |

Para escolher outro arquivo de saída, use `--csv`, por exemplo:

```powershell
python tema_3.py --rapido --csv demonstracao.csv
```

O modo `--rapido` serve apenas para demonstração e **não substitui** os experimentos completos.

## Como funcionam os algoritmos

### Versão ingênua

A função `notas_proximas_ingenua(notas)` verifica todos os pares de posições distintas e calcula a diferença absoluta entre os valores. O número de diferenças calculadas é sempre:

```text
T(n) = n(n - 1) / 2
```

Portanto, sua complexidade é **Θ(n²)**. A contagem não depende da ordem nem dos valores das notas.

### Versão esperta

A função `notas_proximas_esperta(notas)` ordena os valores usando o `mergesort` da base e, em seguida, compara apenas os vizinhos. Depois da ordenação, existe sempre um par de diferença mínima entre elementos consecutivos.

A contagem considera duas etapas: comparações durante a ordenação e diferenças na varredura final. A função `notas_proximas_esperta_detalhada(notas)` devolve esses contadores separadamente. A complexidade total é **Θ(n log n)**.

As duas soluções devolvem `(resultado, contagem)`, sendo o resultado `(menor_nota, maior_nota, diferenca)`. Se a lista tiver menos de duas notas, retornam `(None, 0)`. Em caso de empate, escolhem o menor par em ordem lexicográfica. Nenhuma das soluções modifica a lista original ou interrompe a busca ao encontrar diferença zero.

**Importante:** os contadores representam as operações definidas para o trabalho, não o tempo em segundos nem todas as instruções executadas pelo Python. Na versão esperta, são somadas comparações da ordenação e diferenças da varredura.

## Experimentos e resultados

Foram avaliados três cenários:

- **Melhor caso:** lista preenchida com zeros.
- **Pior caso com valores distintos:** entrada construída para exigir o máximo de comparações do `mergesort` sobre inteiros distintos. Para tamanhos acima de 101, essa série não representa necessariamente o pior caso com notas restritas a 0–100.
- **Caso médio:** 30 listas por tamanho, com notas inteiras sorteadas entre 0 e 100, usando sementes reproduzíveis.

Ambas as versões foram medidas com **100, 200, 400, 800 e 1.600** elementos. A versão esperta também foi testada com **12.500, 25.000, 50.000 e 100.000** elementos.

| n | Ingênua | Esperta: melhor | Esperta: média | Esperta: pior |
| ---: | ---: | ---: | ---: | ---: |
| 100 | 4.950 | 415 | 640,87 | 672 |
| 200 | 19.900 | 931 | 1.479,10 | 1.544 |
| 400 | 79.800 | 2.063 | 3.354,97 | 3.488 |
| 800 | 319.600 | 4.527 | 7.518,47 | 7.776 |
| 1.600 | 1.279.200 | 9.855 | 16.621,00 | 17.152 |

*Fonte: `medicoes.csv`. A coluna da ingênua conta diferenças; as da esperta somam comparações do mergesort e diferenças da varredura. O pior caso da esperta usa inteiros distintos.*

O arquivo `medicoes.csv` reúne **1.056 registros de dados**, além do cabeçalho `versao,n,contagem`. São 960 medições individuais do caso médio e 96 registros de resumo. Os dados foram reproduzidos e conferidos sem diferenças. As fórmulas e as medições também foram comparadas no relatório acadêmico.

O **teste do dobro** ajuda a observar o crescimento das operações: a razão da versão ingênua se aproxima de 4, enquanto a da esperta se aproxima de 2, com a variação esperada para `n log n`. As contagens permitem comparar o crescimento, mas não devem ser tratadas como medidas diretas de velocidade.

## Testes

A suíte contém **16 testes automatizados**, incluindo casos com listas vazias, uma única nota, valores repetidos, negativos, empates, entradas ordenadas e invertidas.

Também foram utilizadas 364 listas pequenas examinadas exaustivamente, 1.000 entradas aleatórias reproduzíveis, conferência dos contadores e testes do modo interativo. Um verificador independente nos testes compara os resultados das duas soluções com a busca por todos os pares.

Para repetir a suíte:

```powershell
python -m unittest testes_tema_3 testes_interativo -v
```

## Funções misteriosas

Como parte da atividade proposta na disciplina, criamos duas funções para que outra equipe analise suas operações e estime a complexidade:

- `misteriosas_para_troca.py`: versão destinada à troca, com a operação marcada por `# ←` e sem a contagem pronta.
- `misteriosas_criadas.py`: versão instrumentada, usada para conferir os resultados e as contagens.

Os arquivos são módulos Python. Executá-los diretamente não imprime resultados. Para testar a versão instrumentada:

```powershell
python -c "from misteriosas_criadas import misteriosa_a, misteriosa_b; print('A:', misteriosa_a(10)); print('B:', misteriosa_b(10))"
```

O gabarito não faz parte deste repositório. A dinâmica de troca e a análise das funções recebidas ainda dependem das orientações do professor.

## Arquivos principais

```text
trabalho_base.py          # Funções disponibilizadas na base da disciplina
tema_3.py                # Algoritmos e modo interativo
experimentos_tema_3.py   # Geração das medições e tabelas
testes_tema_3.py         # Testes dos algoritmos e experimentos
testes_interativo.py     # Testes do modo interativo
misteriosas_criadas.py   # Funções misteriosas instrumentadas
misteriosas_para_troca.py # Versão destinada à troca
medicoes.csv             # Resultados completos dos experimentos
README.md
```

Os PDFs do professor foram mantidos localmente na pasta `referencias/` e não são publicados no repositório.

## Origem da base

O professor disponibilizou o código-base em PDF. Como não tínhamos o arquivo `.py` separado, organizamos esse código em `trabalho_base.py` para conseguir executá-lo no projeto.

Mantivemos as funções e a lógica apresentadas no material, incluindo o `mergesort`, o `teste_do_dobro` e o `salvar_csv`. Depois, executamos os exemplos da base e conferimos a geração das tabelas e do CSV.

## Situação do projeto

A implementação das duas soluções, o modo interativo, os testes, os experimentos e a análise matemática estão concluídos. O relatório acadêmico foi preparado com os resultados obtidos.

A atividade de troca das funções misteriosas ainda aguarda a explicação do professor. A apresentação em slides também faz parte das próximas etapas.

O repositório permanece **privado**, com acesso mediante convite. Foram utilizadas ferramentas de IA como apoio ao desenvolvimento, à revisão e à documentação; esse uso é informado no relatório acadêmico.
