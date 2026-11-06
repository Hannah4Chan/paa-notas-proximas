# Análise matemática: as duas notas mais próximas

## 1. Problema e convenção de contagem

Dada uma lista de n notas inteiras, queremos dois valores cuja diferença absoluta seja mínima. Posições diferentes podem ter a mesma nota. Havendo empate na diferença, escolhemos o par com a menor primeira nota e, depois, a menor segunda nota. Cada par é apresentado em ordem crescente.

Esta análise corresponde às funções de `tema_3.py`, ao mergesort de `trabalho_base.py` e aos experimentos de `experimentos_tema_3.py`. Os dados citados vêm de `medicoes.csv`, no estado do commit `9a739d2068a8ac48fa30b61b79c6fea38ead2dde`. É um material de estudo, anterior ao relatório acadêmico final.

As funções principais retornam `((menor, maior, diferenca), contagem)`. Para n=0 ou n=1, retornam `(None, 0)`. A função detalhada da versão esperta retorna `(resultado, comparacoes_ordenacao, diferencas_varredura)`; sem par, retorna `(None, 0, 0)`.

A operação básica da ingênua é o cálculo de uma diferença absoluta. Na esperta, há duas operações básicas distintas: uma comparação de elementos na intercalação e uma diferença de notas vizinhas. Seu total é a soma dessas contagens, conforme a metodologia do trabalho. Não se trata de segundos nem da contagem de todas as instruções Python.

Controles dos laços, testes de desempate, acessos, cópias de listas e atualizações do melhor resultado não são acrescentados aos contadores. A análise assintótica usa o modelo usual de custo constante para comparar e operar sobre as notas inteiras utilizadas. O custo de geração das entradas, testes e exportação do CSV não faz parte do contador dos algoritmos.

## 2. Versão ingênua: todos os pares

### 2.1. Dos laços ao somatório

O primeiro laço percorre `i` de 0 a n-1. Para cada i, o segundo percorre `j` de i+1 a n-1. Quando i=n-1, não existe j válido; por isso o somatório pode terminar em n-2:

$$
T_I(n)=\sum_{i=0}^{n-2}\sum_{j=i+1}^{n-1}1,\qquad n\geq2.
$$

O termo 1 representa uma diferença calculada para o par de posições (i,j). A condição i<j evita comparar uma posição consigo mesma e evita contar duas vezes o mesmo par.

Para um i fixo, há n-1-i escolhas de j. Logo:

$$
\begin{aligned}
T_I(n)&=\sum_{i=0}^{n-2}(n-1-i)\\
      &=(n-1)+(n-2)+\cdots+1\\
      &=\sum_{k=1}^{n-1}k=\frac{n(n-1)}2.
\end{aligned}
$$

A soma dos inteiros de 1 a n-1 tem n-1 termos; o primeiro e o último somam n. Emparelhar os termos, ou tomar a média dos extremos e multiplicar pela quantidade, produz n(n-1)/2.

### 2.2. Exemplos pequenos

| n | Pares de índices | Diferenças calculadas |
|---:|---|---:|
| 3 | (0,1), (0,2), (1,2) | 2+1=3 |
| 4 | (0,1), (0,2), (0,3), (1,2), (1,3), (2,3) | 3+2+1=6 |
| 5 | Quatro pares com i=0, três com i=1, dois com i=2 e um com i=3 | 4+3+2+1=10 |

Com as notas `[10, 3, 11, 4]`, são seis diferenças, mesmo que um par de diferença 1 apareça cedo. Com `[9, 9, 2, 2]`, também são seis: encontrar diferença zero não encerra o algoritmo.

### 2.3. Melhor, médio e pior caso

Existe, para a versão ingênua, um melhor caso diferente do pior? Não, considerando o número de diferenças calculadas: toda entrada de tamanho n produz exatamente n(n-1)/2 diferenças. Isso não significa que todas as entradas retornem o mesmo par ou a mesma diferença mínima.

Os limites dos laços dependem somente de n. Nenhuma condição sobre os valores desvia ou interrompe esses laços. Assim, a contagem é a mesma para notas ordenadas, embaralhadas, distintas ou repetidas. Qualquer distribuição de entradas de tamanho n tem a mesma contagem média, pois todas as entradas têm o mesmo T_I(n).

Para n>=2:

$$
\frac{n^2}{4}\leq\frac{n(n-1)}2\leq\frac{n^2}{2}.
$$

As duas cotas diferem apenas por constantes. Portanto, melhor caso, caso médio e pior caso são todos **Θ(n²)**. Para n=0 ou n=1, nenhum par é examinado e a própria fórmula n(n-1)/2 também produz zero. As afirmações assintóticas descrevem o crescimento quando n aumenta, não esses casos isolados.

Uma parada antecipada ao encontrar zero seria uma implementação diferente. O código existente não contém essa parada e sua fórmula exata não a pressupõe.

## 3. Versão esperta: ordenar e varrer

A função detalhada primeiro chama `mergesort(notas)`, que devolve uma nova lista ordenada e o número de comparações. Depois executa `for i in range(1, len(ordenadas))`, comparando os valores das posições i-1 e i.

Se C(v) é o número de comparações da ordenação da entrada v, a contagem total é:

$$
T_E(v)=C(v)+V(n),\qquad
V(n)=\begin{cases}0,&n<2,\\n-1,&n\geq2.\end{cases}
$$

Na lista ordenada, `b-a` já é não negativo, então não é necessário aplicar `abs`. Cada iteração calcula exatamente uma diferença. Para n>=2, n/2<=n-1<=n, portanto **V(n)=Θ(n)**.

A varredura nunca para ao encontrar zero. O desempate é verificado explicitamente e o número de diferenças continua sendo n-1 em todos os cenários. As entradas originais não são modificadas por nenhuma das versões.

A ordenação desta implementação é Θ(n log n), inclusive no melhor caso. Somar a varredura linear não muda essa classe:

$$
T_E=\Theta(n\log n)+\Theta(n)=\Theta(n\log n).
$$

A justificativa das cotas da ordenação aparece a seguir. Contar apenas V(n) classificaria somente a segunda fase e deixaria de fora a parte dominante da solução.

## 4. Comparações do mergesort

### 4.1. Divisão e intercalação reais

Para uma lista com n>=2 elementos, o código calcula `meio = len(v) // 2`. A esquerda tem a=floor(n/2) elementos e a direita tem b=ceil(n/2). Piso significa arredondar para baixo; teto, para cima. Por exemplo, para n=5, a=2 e b=3; para n=4, a=b=2.

As metades são ordenadas recursivamente. Na intercalação, o contador cresce uma vez por avaliação de `esquerda[i] <= direita[j]`. Cada comparação envia um elemento ao resultado. O laço termina assim que uma metade acaba; o restante é copiado por `extend`, sem novas comparações contadas.

Para acabar uma metade, é preciso retirar todos os seus elementos. Portanto, o mínimo de comparações dessa intercalação é min(a,b)=a. O máximo é n-1: nessa altura já saiu tudo, exceto um elemento; não é possível continuar comparando duas metades não vazias.

### 4.2. Recorrências exatas e entradas que atingem os extremos

Definimos B(n) como o mínimo e W(n) como o máximo de comparações sobre entradas inteiras de tamanho n. As chamadas de tamanho zero ou um não comparam elementos:

$$
B(0)=B(1)=W(0)=W(1)=0.
$$

Para n>=2:

$$
B(n)=B(\lfloor n/2\rfloor)+B(\lceil n/2\rceil)+\lfloor n/2\rfloor,
$$

$$
W(n)=W(\lfloor n/2\rfloor)+W(\lceil n/2\rceil)+n-1.
$$

O formato da árvore de recursão depende apenas do tamanho da entrada, pois os cortes não dependem das notas. Em cada intercalação de tamanho s, o número de comparações fica entre floor(s/2) e s-1. Somando esses limites em toda a árvore, obtemos as cotas B(n) e W(n). As construções abaixo atingem cada extremo em todas as intercalações ao mesmo tempo; por isso as recorrências descrevem o mínimo e o máximo reais, e não apenas limites que talvez sejam inalcançáveis.

O gerador `melhor_caso(n)` produz n zeros. Como o mergesort usa `<=`, os empates sempre retiram da esquerda. A esquerda acaba após exatamente a comparações, em todos os nós da recursão. Isso atinge B(n), inclusive para n ímpar. Uma lista crescente também atinge esse mínimo.

O gerador `pior_caso(n)` começa com os valores distintos de 0 a n-1. Em cada construção recursiva, os valores de índices ímpares vão para a metade esquerda e os de índices pares para a direita. A esquerda fica com a elementos, como exige o corte do mergesort. Depois de ordenadas, as metades se alternam e só uma das duas acaba quando resta um único elemento no conjunto, exigindo n-1 comparações. A mesma construção dentro de cada metade faz todos os nós atingirem o máximo simultaneamente.

Por exemplo, `pior_caso(5)` produz `[3, 1, 2, 4, 0]`. As metades da raiz, depois de ordenadas, são `[1, 3]` e `[0, 2, 4]`: a intercalação retira 0, 1, 2 e 3 com quatro comparações e copia o 4 restante. Uma lista invertida não foi presumida como pior caso.

### 4.3. Árvore pequena: n=5

A árvore mostra tamanhos das chamadas, não notas:

```text
                 5
              /     \
             2       3
            / \     / \
           1   1   1   2
                      / \
                     1   1
```

| Nós que intercalam | Quantidade | Custo local mínimo por nó | Custo local máximo por nó |
|---|---:|---:|---:|
| Tamanho 5 | 1 | 2 | 4 |
| Tamanho 3 | 1 | 1 | 2 |
| Tamanho 2 | 2 | 1 | 1 |
| Total da árvore | | B(5)=2+1+2=5 | W(5)=4+2+2=8 |

As folhas têm tamanho um e custo de comparação zero. A árvore não é completa em todos os níveis, o que explica por que pisos e tetos importam nas contagens exatas.

### 4.4. Forma fechada do pior caso

Seja h=ceil(log₂ n), para n>=2, considerando a raiz com profundidade zero. O corte inteiro de uma lista de tamanho s produz floor(s/2) elementos à esquerda e ceil(s/2) à direita. Se s for ímpar, as duas metades diferem por um elemento; se for par, têm o mesmo tamanho. Repetindo esses cortes, os subproblemas na profundidade d, enquanto nenhum ramo tiver terminado, têm tamanhos floor(n/2^d) ou ceil(n/2^d). Isso também pode ser verificado por indução: dividir novamente esses dois tamanhos arredondados produz os dois tamanhos arredondados do nível seguinte.

Até a profundidade h-2 não há tamanho um; na profundidade h-1 há apenas tamanhos um ou dois. Portanto cada folha está em h-1 ou h. Defina x como o número de folhas na profundidade h-1 e y como o número de folhas na profundidade h. Como cada folha representa um elemento, x+y=n.

Na profundidade h-1 existem 2^(h-1) nós: x deles já são folhas e os restantes têm tamanho dois. Cada nó de tamanho dois gera duas folhas na profundidade h, então há y/2 desses nós. Assim:

$$
x+\frac y2=2^{h-1}\quad\Longrightarrow\quad2x+y=2^h.
$$

Juntando essa equação com x+y=n, obtemos x=2^h-n e y=2n-2^h. Para n=5, temos h=3, x=3 folhas na profundidade 2 e y=2 folhas na profundidade 3. São exatamente as folhas da árvore da seção 4.3.

A soma das profundidades das folhas é:

$$
D=(2^h-n)(h-1)+(2n-2^h)h=nh-2^h+n.
$$

Cada folha participa de uma intercalação por ancestral. Portanto, somar os tamanhos dos subproblemas de todos os nós internos também resulta em D. Existem n-1 nós internos. Como o custo máximo em um nó de tamanho s é s-1, temos:

$$
W(n)=D-(n-1)=nh-2^h+1.
$$

No exemplo n=5, D=3×2+2×3=12. Há n-1=4 nós internos, portanto W(5)=12-4=8, de acordo com a árvore e sua soma de custos locais.

Substituindo h:

$$
\boxed{W(n)=n\lceil\log_2 n\rceil-2^{\lceil\log_2 n\rceil}+1},\qquad n\geq2.
$$

Para n=5, h=3 e W(5)=5·3-8+1=8. Para n=8, h=3 e W(8)=24-8+1=17. Como h=log₂ n+O(1) e 2^h=O(n), obtemos W(n)=n log₂ n+O(n), logo W(n)=Θ(n log n).

### 4.5. Melhor caso para potências de dois e classe geral

Se n=2^k, há k níveis de intercalação. Em cada nível, os tamanhos somam n e cada nó usa metade de seu tamanho em comparações mínimas. O custo mínimo por nível é n/2. Assim:

$$
\boxed{B(n)=\frac n2\log_2 n}\quad\text{quando }n=2^k,\ n\geq2.
$$

Por exemplo, B(4)=4 e B(8)=12. Essa fórmula especial não deve ser aplicada a qualquer n: para n=5, a recorrência dá B(5)=5, enquanto (5/2)log₂5 é aproximadamente 5,805.

Para justificar a classe geral sem supor uma potência de dois, observe que, em todo nó interno de tamanho s>=2:

$$
\frac{s-1}{2}\leq\lfloor s/2\rfloor\leq s-1.
$$

Somando sobre a mesma árvore de divisões:

$$
\frac{W(n)}2\leq B(n)\leq W(n).
$$

Portanto B(n)=Θ(n log n). Para qualquer entrada v, B(n)<=C(v)<=W(n). Isso também limita a expectativa sob qualquer distribuição de entradas do mesmo tamanho. Melhor, médio e pior caso dessa implementação têm classe Θ(n log n), embora suas constantes e contagens exatas sejam diferentes. O total com a varredura mantém essa classe nos três casos.

## 5. Por que basta examinar vizinhos

### 5.1. Demonstração formal

Ordenar apenas reorganiza as ocorrências das notas: não altera seus valores nem a quantidade de vezes que cada valor aparece. Cada par de posições distintas da lista original corresponde a um par de ocorrências distintas na lista ordenada, com os mesmos valores e a mesma diferença absoluta, e vice-versa. Assim, os pares de valores possíveis e a solução escolhida pelo desempate são preservados.

Considere a lista ordenada a₀<=a₁<=...<=aₙ₋₁, com n>=2. Defina as lacunas consecutivas:

$$
d_k=a_{k+1}-a_k\geq0,\qquad 0\leq k\leq n-2.
$$

Para quaisquer i<j, o cancelamento dos termos intermediários dá a identidade telescópica:

$$
a_j-a_i=(a_{i+1}-a_i)+\cdots+(a_j-a_{j-1})
          =\sum_{k=i}^{j-1}d_k.
$$

Como há pelo menos uma parcela e todas são não negativas, a soma é maior ou igual a cada parcela. Seja g=min(d₀,...,dₙ₋₂). Então todo par de posições i<j satisfaz a_j-a_i>=g. Logo a menor diferença entre todos os pares, chamada δ, satisfaz δ>=g.

Por outro lado, pares vizinhos são pares válidos do problema. O vizinho que realiza g é um candidato, portanto δ<=g. As duas desigualdades provam:

$$
\boxed{\delta=\min_{0\leq k\leq n-2}(a_{k+1}-a_k)}.
$$

Assim, **existe um par ótimo entre vizinhos**. A afirmação não exige que todo par de posições ótimo seja vizinho: em `[2, 2, 2]`, as posições 0 e 2 também formam um par ótimo, mas o mesmo resultado de valores `(2, 2)` já é encontrado em posições vizinhas.

### 5.2. Repetições e desempate lexicográfico

Se δ=0, algum valor aparece pelo menos duas vezes. Depois da ordenação, todas as ocorrências desse valor formam um bloco contíguo, que contém vizinhos iguais. Se houver vários valores repetidos, o menor par ótimo em ordem lexicográfica é `(x, x)`, onde x é o menor valor repetido. Esse par aparece na varredura.

Se δ>0, não há notas repetidas em toda a lista. Um par não vizinho contém pelo menos duas lacunas, cada uma >=δ. Sua diferença seria >=2δ>δ, então não pode ser ótimo. Nesse caso todos os pares ótimos são vizinhos, inclusive o menor deles em ordem lexicográfica.

Em ambos os casos, o conjunto examinado pela versão esperta contém o par que deve vencer o desempate. No código, a diferença é comparada primeiro. Se empatar, `candidato[:2] < melhor[:2]` escolhe as menores notas. Portanto a prioridade matemática é `(diferença, primeira nota, segunda nota)`, embora o resultado seja armazenado como `(primeira nota, segunda nota, diferença)`.

A versão ingênua normaliza cada par em ordem crescente e aplica a mesma prioridade. Após cada iteração, ambas mantêm o melhor candidato entre os já examinados. Como a ingênua visita todos os pares e a esperta visita os vizinhos que contêm o vencedor global, as duas retornam o mesmo resultado.

### 5.3. Exemplo e intuição

Ordenando `[10, 3, 11, 4]`, obtemos `[3, 4, 10, 11]`. As lacunas são 1, 6 e 1. A diferença entre 3 e 11 é 1+6+1=8. O mínimo global é 1, encontrado pelos vizinhos `(3, 4)` e `(10, 11)`. O desempate escolhe `(3, 4, 1)`.

Na reta, ir de uma nota até outra mais distante significa atravessar todos os intervalos entre elas. Como nenhum intervalo tem comprimento negativo, atravessar vários não pode ser mais curto que cada um dos intervalos atravessados. Por isso procurar a menor lacuna já resolve o problema.

## 6. Confronto entre fórmulas e dados reais

As tabelas abaixo foram conferidas com `medicoes.csv`. Na ingênua, os cenários `melhor`, `pior_distintos` e cada amostra de `medio` têm a mesma contagem. A varredura também independe do cenário.

| n | n(n-1)/2 teórico | Ingênua medida | n-1 teórico | Varredura medida |
|---:|---:|---:|---:|---:|
| 100 | 4.950 | 4.950 | 99 | 99 |
| 400 | 79.800 | 79.800 | 399 | 399 |
| 1.600 | 1.279.200 | 1.279.200 | 1.599 | 1.599 |

| n | B(n) pela recorrência | Ordenação medida: melhor | W(n) pela recorrência e forma fechada | Ordenação medida: pior_distintos |
|---:|---:|---:|---:|---:|
| 100 | 316 | 316 | 573 | 573 |
| 400 | 1.664 | 1.664 | 3.089 | 3.089 |
| 1.600 | 8.256 | 8.256 | 15.553 | 15.553 |

Na última coluna teórica, por exemplo, W(100)=100·7-128+1=573; W(400)=400·9-512+1=3.089; W(1600)=1600·11-2048+1=15.553. Esses tamanhos não são potências de dois; B(n) foi obtido pela recorrência, não pela fórmula especial da seção 4.5.

| n | Total melhor: B(n)+n-1 | Total pior: W(n)+n-1 | Média da ordenação | Média total medida |
|---:|---:|---:|---:|---:|
| 100 | 415 | 672 | 16.256/30 = 541,8666... | 19.226/30 = 640,8666... |
| 400 | 2.063 | 3.488 | 88.679/30 = 2.955,9666... | 100.649/30 = 3.354,9666... |
| 1.600 | 9.855 | 17.152 | 450.660/30 = 15.022 | 498.630/30 = 16.621 |

Os totais extremos correspondem aos registros `esperta/melhor/total` e `esperta/pior_distintos/total`. As médias correspondem aos registros `esperta/medio/ordenacao/media` e `esperta/medio/total/media`. As frações mostram as somas das 30 contagens individuais, evitando arredondar antes dos cálculos. O CSV representa as médias com números de ponto flutuante, sujeitos à precisão usual desse formato.

Não houve divergência entre fórmulas exatas e contagens medidas nesses confrontos. Θ(n²) e Θ(n log n), porém, não especificam uma quantidade exata de operações. Por exemplo, n log₂n não precisa ser igual a W(n): o termo linear e o teto do log fazem parte da expressão exata, embora não alterem a classe assintótica.

## 7. Interpretação do teste do dobro

### 7.1. O que a função da base calcula

`teste_do_dobro` recebe uma função que fornece c(n) e imprime as razões c/log₂n, c/n, c/(n log₂n), c/n² e c/n³. A coluna `dobro` é a contagem atual dividida pela anterior. Ela corresponde a c(n)/c(n/2) somente quando os tamanhos consecutivos realmente dobram.

O experimento usa as séries 100, 200, 400, 800, 1600 e, separadamente, 12500, 25000, 50000, 100000. O primeiro valor de cada série recebe `-` na coluna `dobro`; não há uma razão artificial entre 1600 e 12500. Cada cenário e cada fase têm tabela própria.

Para funções-modelo c(n)~αf(n), com α>0, a coluna cujo denominador é f(n) tende à constante α. A tabela resume os outros comportamentos quando n cresce:

| Modelo f(n) | c/log₂n | c/n | c/(n log₂n) | c/n² | c/n³ | c(2n)/c(n) |
|---|---|---|---|---|---|---|
| log₂n | Constante positiva | 0 | 0 | 0 | 0 | 1 |
| n | Cresce | Constante positiva | 0 | 0 | 0 | 2 |
| n log₂n | Cresce | Cresce como log n | Constante positiva | 0 | 0 | 2 |
| n² | Cresce | Cresce | Cresce | Constante positiva | 0 | 4 |
| n³ | Cresce | Cresce | Cresce | Cresce | Constante positiva | 8 |

Uma razão que tende a zero não identifica por si só a classe: dividir uma contagem linear por n³ também dá zero. O sinal procurado é uma razão que fica próxima de uma constante positiva e finita ao longo de vários tamanhos. Também é preciso distinguir esse indício da prova matemática.

Θ descreve a ordem de crescimento, mas não garante, sozinha, que uma razão se aproxime de uma constante. Os limites da tabela valem para os modelos indicados. No mergesort, as fórmulas dos extremos justificam a classe; as médias medidas ajudam a observar o crescimento, sem fornecer uma expectativa exata.

### 7.2. Ingênua: por que o dobro tende a 4

Usando a fórmula exata, para n>=2:

$$
\frac{T_I(2n)}{T_I(n)}
=\frac{(2n)(2n-1)}{n(n-1)}
=4+\frac{2}{n-1}\longrightarrow4.
$$

Além disso, T_I(n)/n²=(1-1/n)/2 tende a 1/2. Nos dados:

| n | c/n² | Dobro em relação ao tamanho anterior |
|---:|---:|---:|
| 100 | 0,495000 | - |
| 200 | 0,497500 | 4,020202 |
| 400 | 0,498750 | 4,010050 |
| 800 | 0,499375 | 4,005013 |
| 1.600 | 0,499688 | 4,002503 |

As razões foram calculadas com as contagens inteiras, e arredondadas somente nesta apresentação. A estabilização em torno de 0,5 e o dobro próximo de 4 concordam com a demonstração quadrática.

### 7.3. Ordenação e total: aproximação lenta de 2

Para o modelo c(n)=αn log₂n:

$$
\frac{c(2n)}{c(n)}=2\frac{\log_2n+1}{\log_2n}
=2+\frac2{\log_2n}\longrightarrow2.
$$

O termo adicional diminui lentamente porque o denominador é um logaritmo. Por isso uma razão próxima de 2 não basta para concluir que um algoritmo seja linear.

No pior caso, a forma fechada dá W(n)=n log₂n+O(n). Para potências de dois, o melhor caso é exatamente (n/2)log₂n. Para n geral, a soma de floor(s/2) por nó é metade da soma dos tamanhos, menos no máximo metade do número de nós; logo B(n)=(n/2)log₂n+O(n). Assim, os extremos têm a forma n log n com termos lineares menores e suas razões de dobro tendem a 2. Somar n-1 ao custo da ordenação apenas modifica esse termo linear.

Para o caso médio, os valores reais são:

| n | Ordenação média / (n log₂n) | Dobro da ordenação média | Total médio / (n log₂n) | Dobro do total médio |
|---:|---:|---:|---:|---:|
| 100 | 0,815591 | - | 0,964600 | - |
| 200 | 0,837339 | 2,362389 | 0,967509 | 2,307968 |
| 400 | 0,854933 | 2,309169 | 0,970333 | 2,268249 |
| 800 | 0,870952 | 2,273188 | 0,974515 | 2,240996 |
| 1.600 | 0,882082 | 2,235594 | 0,975974 | 2,210690 |
| 12.500 | 0,906561 | - | 0,980033 | - |
| 25.000 | 0,912733 | 2,161571 | 0,981178 | 2,149464 |
| 50.000 | 0,917945 | 2,149099 | 0,982007 | 2,138701 |
| 100.000 | 0,922565 | 2,138836 | 0,982770 | 2,129780 |

Os cálculos usaram as médias completas do CSV; os números desta tabela foram arredondados a seis casas somente no final. A base imprime menos casas em algumas colunas. As razões de dobro diminuem e a normalização por n log₂n varia cada vez menos nesta série. Isso é compatível com a análise, mas estes nove tamanhos e 30 amostras por tamanho não demonstram um limite numérico exato da média.

A coluna c/n ainda cresce: para a ordenação média, passa de 5,418667 em n=100 para 15,323472 em n=100000. Isso ajuda a distinguir seu comportamento do da varredura linear.

### 7.4. Varredura linear

Como V(n)=n-1, temos:

$$
\frac{V(n)}n=1-\frac1n\longrightarrow1,\qquad
\frac{V(2n)}{V(n)}=\frac{2n-1}{n-1}=2+\frac1{n-1}\longrightarrow2.
$$

Em n=100, 400 e 1600, V(n)/n vale 0,99, 0,9975 e 0,999375. O dobro nas linhas n=200, 400 e 1600 vale aproximadamente 2,010101, 2,005025 e 2,001252. Para n=100000, V(n)=99999 e V(n)/n=0,99999. A coluna c/n estabiliza; dividir por n log₂n, n² ou n³ faz a razão tender a zero.

## 8. O caso médio e as notas repetidas

A hipótese experimental é de notas inteiras uniformes no conjunto {0,...,100}, amostradas com reposição pelo gerador `aleatorio` da base. São 30 entradas por tamanho e sementes:

```text
semente(n,r) = 202600000 + 100*n + r, com r=0,...,29
```

Por exemplo, em n=100, as sementes vão de 202610000 a 202610029; em n=1600, de 202760000 a 202760029. Cada amostra é usada pelas duas versões quando n pertence à série comum. A sequência é reproduzível. Há 270 amostras na versão esperta e 150 na ingênua, que reutiliza as amostras dos cinco tamanhos comuns.

Para uma fase, a média experimental é:

$$
\overline C(n)=\frac1{30}\sum_{r=0}^{29}C(v_{n,r}).
$$

Ela estima a expectativa sob a hipótese declarada, mas não é uma fórmula exata para E[C]. Os limites B(n)<=C(v)<=W(n) justificam a classe assintótica também para a expectativa; não fornecem seu valor exato. Trinta amostras não provam definitivamente uma distribuição nem dispensam a análise matemática.

Existem apenas 101 valores possíveis. Pelo princípio da casa dos pombos, se n>=102, pelo menos duas notas são iguais. Portanto a diferença mínima é necessariamente zero. Para n<=101, também podem existir repetições, mas não são obrigatórias.

Esse resultado não torna inútil medir as operações. A ingênua examina todos os pares mesmo depois de achar zero; a esperta ordena a lista inteira e percorre todos os n-1 vizinhos. As repetições podem afetar quantas comparações ocorrem na intercalação, inclusive porque `<=` favorece a esquerda nos empates, mas não eliminam nenhuma das fases. O contador estuda o trabalho do algoritmo, não apenas a variedade da resposta final.

## 9. Pior caso absoluto e domínio restrito

A série `pior_distintos` usa uma permutação de 0 a n-1, com todos os valores diferentes. Ela atinge W(n) e, com a varredura, W(n)+n-1. Isso demonstra o pior caso absoluto desta implementação sobre entradas inteiras.

Para n>101, essa construção sai do intervalo de notas de 0 a 100. Portanto ela não deve ser apresentada como uma turma real nesse domínio. Por outro lado, o fato de existirem apenas 101 valores não prova, sozinho, que atingir W(n) com repetições seja impossível. Determinar o máximo exato sob essa restrição exige uma demonstração própria, que não foi feita aqui.

A formulação precisa é: a construção distinta comprova o máximo geral; a série média representa a hipótese restrita de notas; não se confundem as duas distribuições nem se atribui ao domínio restrito um máximo ainda não demonstrado.

## 10. Conteúdo extra: por que vizinhos não bastam no plano

Em duas dimensões, cada aluno é um ponto (AV1, AV2). Adotando a distância euclidiana, considere:

```text
P = (0, 0)
Q = (2, 2)
R = (1, 100)
S = (100, 1)
```

| Par | Distância ao quadrado |
|---|---:|
| P,Q | 8 |
| P,R | 10001 |
| P,S | 10001 |
| Q,R | 9605 |
| Q,S | 9605 |
| R,S | 19602 |

O par mais próximo é P,Q, com distância √8, aproximadamente 2,828. Ordenando pela primeira coordenada, a ordem é P,R,Q,S. Os pares vizinhos têm distâncias ao quadrado 10001, 9605 e 9605: nenhum é o par ótimo. Ordenando pela segunda coordenada, a ordem é P,S,Q,R, e o par ótimo continua não vizinho. Não há empate nas coordenadas que torne a ordem ambígua.

Na reta, a diferença entre dois valores é a soma das lacunas não negativas entre eles. No plano, um ponto pode ficar entre outros dois na ordem de uma coordenada e estar muito longe na outra. Assim, ordenar por uma coordenada e examinar somente vizinhos pode deixar passar o par mais próximo, como ocorre neste exemplo. Isso mostra por que essa aplicação direta da estratégia unidimensional não resolve o problema em geral.

## 11. Conferências e fontes locais

As contagens inteiras e as médias citadas foram lidas de `medicoes.csv`, de cabeçalho `versao,n,contagem`. Os registros individuais do caso médio identificam repetição e semente; os registros `/media` permitem conferir as médias usadas nas tabelas. O CSV contém 1056 registros, além do cabeçalho.

Foram conferidos os exemplos pequenos, as recorrências contra `comparacoes_extremas`, as contagens de `mergesort(melhor_caso(n))` e `mergesort(pior_caso(n))`, os três tamanhos principais e as razões das duas séries. A enumeração de casos pequenos e os testes de correção complementam as demonstrações; não as substituem.

Fontes do projeto:

- `referencias/Trabalho_PAA_Contagem_Operacoes.pdf`: Tema 3 e roteiro experimental.
- `referencias/trabalho_base.pdf` e `trabalho_base.py`: mergesort, instrumentação e teste do dobro.
- `tema_3.py`: algoritmos e desempate analisados.
- `experimentos_tema_3.py`: geradores, recorrências, sementes e médias.
- `testes_tema_3.py`: verificações automatizadas.
- `medicoes.csv`: contagens individuais e resumos experimentais.

O texto não resolve as funções misteriosas nem constitui o relatório final.
