# As duas notas mais próximas

Trabalho individual de Projeto e Análise de Algoritmos sobre o Tema 3, As duas notas mais próximas. O objetivo é encontrar dois valores de uma lista de notas cuja diferença absoluta seja mínima, contando as operações realizadas.

O projeto contém os algoritmos e os experimentos de contagem de operações. A escolha do Tema 3 e a adaptação das funções misteriosas para trabalho individual ainda dependem de confirmação do professor. As regras originais não foram consideradas oficialmente alteradas.

## Algoritmos e contratos

- `notas_proximas_ingenua(notas)` examina todas as posições i < j. Retorna `((menor, maior, diferenca), contagem)`. Conta uma diferença por par, exatamente `n * (n - 1) // 2`. Seu custo é O(n²), independentemente da ordem da entrada.
- `notas_proximas_esperta(notas)` usa exclusivamente o mergesort da base e examina todos os vizinhos. Retorna o mesmo resultado e a soma das contagens. Seu custo é O(n log n), incluindo a ordenação.
- `notas_proximas_esperta_detalhada(notas)` retorna `(resultado, comparacoes_ordenacao, diferencas_varredura)`, sem objetos auxiliares. A varredura conta exatamente `n - 1` diferenças para n >= 2.

As funções principais retornam `(None, 0)` quando não há duas notas. A função detalhada retorna `(None, 0, 0)`. A entrada válida é uma lista de inteiros; não há validação de tipos. O caso médio usa notas de 0 a 100. A série de pior caso usa valores distintos de 0 a n-1, identificados separadamente. Os testes também usam inteiros negativos e valores distintos fora desse intervalo.

Em caso de empate, vence o par com menor primeira nota e, depois, menor segunda nota. As notas do resultado aparecem em ordem crescente. Em `[10, 3, 11, 4]`, ambas as versões devolvem `(3, 4, 1)`. Notas iguais em posições distintas são válidas. Nenhuma versão encerra a busca ao encontrar diferença zero ou altera a lista recebida.

O total da versão esperta soma operações de naturezas diferentes: comparações do mergesort e diferenças da varredura. Ele segue a convenção do trabalho, não representa todas as instruções Python. Controle dos laços e desempates não entram nesses contadores.

Depois de ordenar, basta comparar notas vizinhas: um valor intermediário não pode aumentar a proximidade dos extremos. A prova matemática detalhada ficará no relatório.

## Execução

É necessário Python 3, sem bibliotecas externas e sem conexão com a internet.

```powershell
python tema_3.py
python -m unittest testes_tema_3 -v
python trabalho_base.py
```

O primeiro comando executa os oito testes de correção e, se todos passarem, mede os três cenários, imprime 21 tabelas pela função `teste_do_dobro` da base e gera `medicoes.csv` na pasta do projeto. Se um teste falhar, encerra antes de medir. O tempo de execução depende do computador.

O segundo comando executa a suíte completa de 13 métodos, incluindo os testes da infraestrutura experimental. O comando principal executa apenas a classe de correção para evitar que o teste que chama o programa em subprocesso invoque a si mesmo. O terceiro executa os asserts e as duas tabelas demonstrativas originais da base, gerando `medicoes_exemplo.csv` com dez linhas de dados. Esse arquivo é descartável e está no .gitignore; `medicoes.csv` não está ignorado.

Projeto testado com Python 3.14.7 no Windows.

## Estrutura atual

```text
referencias/
    trabalho_base.pdf
    Trabalho_PAA_Contagem_Operacoes.pdf
trabalho_base.py
tema_3.py
experimentos_tema_3.py
testes_tema_3.py
medicoes.csv
README.md
.gitignore
```

A execução também cria caches Python e o CSV demonstrativo, ambos ignorados pelo Git. Os dois PDFs de referência permanecem disponíveis localmente, mas também estão ignorados para evitar publicação automática dos materiais do professor. Não há arquivos vazios para etapas futuras.

## Origem da base

Não existia arquivo Python original na pasta. `trabalho_base.py` foi reconstruído a partir das duas páginas de `referencias/trabalho_base.pdf`. Foram restauradas as quebras de linha e a indentação; os comentários e docstrings legíveis foram restaurados conforme o PDF, preservando os nomes, parâmetros, valores padrão, geradores, contadores e lógica. O mergesort não recebeu otimizações ou mudanças de algoritmo. Foram preservados `teste_do_dobro`, `salvar_csv` e os testes demonstrativos do bloco principal.

A validação executou os três asserts da base, as tabelas e a geração do CSV. Isso não substitui uma comparação com o arquivo .py original, que continua indisponível. Os dois PDFs foram copiados de Downloads sem alteração, com igualdade de SHA-256 verificada.

## Testes e verificações

A suíte mantém os oito métodos de correção e acrescenta cinco métodos para os experimentos:

- Casos de borda: vazio, unitário, dois elementos, ordenado, invertido, todos iguais, repetidos, negativos e empates.
- Desempate obrigatório e contratos para listas sem par.
- 364 listas exaustivas de tamanhos 0 a 5, com valores -1, 0 e 1.
- 1.000 entradas aleatórias, com sementes de 1000 a 1999 e tamanhos de 2 a 80. São quatro grupos de 250 casos: sementes 1000 a 1249 usam `aleatorio` no intervalo 0 a 100; 1250 a 1499, no intervalo 0 a 1000; 1500 a 1749, no intervalo -10000 a 10000; 1750 a 1999 usam `distintos` com deslocamento e passo positivo variados, obtidos por `aleatorio` com a mesma semente. O tamanho é `2 + semente % 79`.
- A contagem efetiva encontrou 1.000 listas distintas, considerando a sequência completa de valores, e 799 resultados distintos. Houve 367 entradas com diferença mínima zero e 633 com diferença positiva. Em 582 entradas houve empate entre pelo menos dois pares de valores diferentes. A unicidade foi medida, não presumida a partir das sementes.
- Contadores em vários tamanhos e ordens, contagens conhecidas e uma entrada de 1.600 notas com semente 2026.

Um oráculo independente enumera combinações de duas posições e usa `min` para escolher por `(diferenca, menor, maior)`. Esses recursos ficam nos testes. A verificação compara o par e a diferença, confere a lista após cada chamada e compara o contador de ordenação com o mergesort da base.

Para `[4, 1, 3, 2]`, a versão ingênua conta 6 diferenças; a esperta conta 5 comparações de ordenação e 3 diferenças, total 8. O caso `[9, 9, 2, 2]` comprova que uma diferença zero não encerra os laços.

As soluções não usam sorted, list.sort, bisect, set, dict, Counter, pertencimento em listas ou min/max para encontrar o par. A base mantém seu DictWriter para exportação CSV e sorted no assert demonstrativo, conforme o material fornecido.

Os testes novos verificam os extremos do mergesort por enumeração de todas as permutações até n=6 e por recorrências em tamanhos maiores; sementes e entradas reproduzíveis; médias e correspondência exata com as tabelas e o CSV; execução do comando em modo rápido; e interrupção antes de medir quando os testes falham. Os testes usam tamanhos pequenos e arquivos temporários na pasta do projeto.

## Experimentos

A execução padrão usa n = 100, 200, 400, 800 e 1600 nas duas versões. A esperta também usa n = 12500, 25000, 50000 e 100000. A ingênua não é executada nesses tamanhos ampliados. As duas séries do teste do dobro são separadas, reiniciando a coluna `dobro` no começo da série ampliada.

- `melhor`: todas as notas são zero. Em cada intercalação do mergesort, a metade esquerda é consumida após o mínimo de comparações.
- `pior_distintos`: permutação de 0 a n-1 construída recursivamente, colocando valores de índices ímpares na metade esquerda e os de índices pares na direita. Depois de ordenadas, as metades se alternam até restar apenas um elemento, exigindo n-1 comparações naquela intercalação. A construção também se aplica às sublistas. Essa série usa inteiros distintos, fora do domínio 0 a 100 para n > 101; representa o extremo do algoritmo sobre inteiros, não um pior caso provado sob o domínio restrito de notas.
- `medio`: 30 amostras por tamanho, geradas por `aleatorio` da base. A hipótese é de notas inteiras independentes, uniformes de 0 a 100, com reposição. Para repetição r = 0 a 29, a semente é `202600000 + 100*n + r`. As duas versões recebem a mesma lista em cada medição aplicável. Repetidos são permitidos; sementes diferentes não são tratadas como prova de listas diferentes.

Na ingênua, melhor, pior e médio têm a mesma contagem de diferenças. A esperta registra `ordenacao`, `varredura` e `total`. O total soma comparações e diferenças, seguindo a convenção do trabalho, sem representar tempo ou todas as instruções executadas.

A medição dos extremos é conferida pelas recorrências, com a = floor(n/2), b = ceil(n/2) e B(0)=B(1)=W(0)=W(1)=0:

```text
B(n) = B(a) + B(b) + a
W(n) = W(a) + W(b) + n - 1
```

Essas verificações não substituem a análise formal do relatório. As contagens medidas não são substituídas pelas fórmulas.

Para uma demonstração parcial:

```powershell
python tema_3.py --rapido
```

Esse modo usa o mesmo medidor, com n = 100 e 200, três amostras por tamanho, sem série ampliada. Imprime um aviso e grava `medicoes_rapidas.csv`, sem substituir `medicoes.csv`. Opcionalmente, `--csv caminho.csv` escolhe outro destino para a execução. O modo rápido não cumpre sozinho o experimento obrigatório.

## Dados em CSV

O arquivo completo `medicoes.csv` contém 1.056 registros de dados, mais o cabeçalho fixo `versao,n,contagem`, e pode ser versionado. É gravado exclusivamente por `salvar_csv` da base. O CSV demonstrativo `medicoes_exemplo.csv` continua separado e ignorado pelo Git.

O campo `versao` identifica algoritmo, cenário e fase. Exemplos:

```text
esperta/pior_distintos/ordenacao
esperta/medio/ordenacao/rep=00/semente=202610000
esperta/medio/ordenacao/media
```

O exemplo de semente corresponde a n=100 e r=0. São 960 registros individuais do caso médio e 96 registros de resumo usados nas tabelas. Para recalcular uma média, selecione o mesmo algoritmo, cenário, fase e n, some os 30 registros `rep=...` e divida por 30. A linha `/media` guarda esse valor sem arredondamento prévio. As razões são calculadas a partir dele; só a exibição da base arredonda. Nos extremos, cada resumo corresponde a uma execução real. Não há medições duplicadas por série, pois seus tamanhos não se sobrepõem.

As contagens podem ser reproduzidas com as sementes registradas. O tempo de execução é apenas uma informação prática e não é usado para classificar os algoritmos.

## Estado e próximas etapas

Concluídos: repositório Git local, cópias dos PDFs, reconstrução e validação da base, algoritmos, contadores separados, testes e experimentos com tabelas e CSV. O código está versionado no [GitHub](https://github.com/Hannah4Chan/paa-notas-proximas). O repositório permanece privado durante o desenvolvimento.

Pendentes: confirmação do professor sobre o tema e a adaptação individual das funções misteriosas, análise formal de melhor e pior caso, funções misteriosas, relatório e slides.

O Codex participou da reconstrução da base, implementação, testes e documentação. A declaração completa de uso de IA será incluída no relatório acadêmico, conforme o enunciado.
