# As duas notas mais próximas

Trabalho individual de Projeto e Análise de Algoritmos sobre o Tema 3, As duas notas mais próximas. O objetivo é encontrar dois valores de uma lista de notas cuja diferença absoluta seja mínima, contando as operações realizadas.

Esta é a implementação inicial. A escolha do Tema 3 e a adaptação das funções misteriosas para trabalho individual ainda dependem de confirmação do professor. As regras originais não foram consideradas oficialmente alteradas.

## Algoritmos e contratos

- `notas_proximas_ingenua(notas)` examina todas as posições i < j. Retorna `((menor, maior, diferenca), contagem)`. Conta uma diferença por par, exatamente `n * (n - 1) // 2`. Seu custo é O(n²), independentemente da ordem da entrada.
- `notas_proximas_esperta(notas)` usa exclusivamente o mergesort da base e examina todos os vizinhos. Retorna o mesmo resultado e a soma das contagens. Seu custo é O(n log n), incluindo a ordenação.
- `notas_proximas_esperta_detalhada(notas)` retorna `(resultado, comparacoes_ordenacao, diferencas_varredura)`, sem objetos auxiliares. A varredura conta exatamente `n - 1` diferenças para n >= 2.

As funções principais retornam `(None, 0)` quando não há duas notas. A função detalhada retorna `(None, 0, 0)`. A entrada válida é uma lista de inteiros; não há validação de tipos. Nos experimentos principais serão usadas notas de 0 a 100. Os testes também usam inteiros negativos e valores distintos fora desse intervalo.

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

O primeiro comando executa os testes e imprime três demonstrações pequenas com os contadores. Se um teste falhar, encerra com código diferente de zero. Ainda não imprime as tabelas experimentais completas nem gera o CSV definitivo.

O segundo comando executa somente os testes. O terceiro executa os asserts e as duas tabelas demonstrativas originais da base, gerando `medicoes_exemplo.csv` com dez linhas de dados. Esse arquivo é descartável e está no .gitignore; `medicoes.csv` não está ignorado.

O projeto foi validado com Python 3.14.7. Os comandos acima funcionam no PowerShell da usuária.

## Estrutura atual

```text
referencias/
    trabalho_base.pdf
    Trabalho_PAA_Contagem_Operacoes.pdf
trabalho_base.py
tema_3.py
testes_tema_3.py
README.md
.gitignore
```

A execução também cria caches Python e o CSV demonstrativo, ambos ignorados pelo Git. Os dois PDFs de referência permanecem disponíveis localmente, mas também estão ignorados para evitar publicação automática dos materiais do professor. Não há arquivos vazios para etapas futuras.

## Origem da base

Não existia arquivo Python original na pasta. `trabalho_base.py` foi reconstruído a partir das duas páginas de `referencias/trabalho_base.pdf`. Foram restauradas as quebras de linha e a indentação; os comentários e docstrings legíveis foram restaurados conforme o PDF, preservando os nomes, parâmetros, valores padrão, geradores, contadores e lógica. O mergesort não recebeu otimizações ou mudanças de algoritmo. Foram preservados `teste_do_dobro`, `salvar_csv` e os testes demonstrativos do bloco principal.

A validação executou os três asserts da base, as tabelas e a geração do CSV. Isso não substitui uma comparação com o arquivo .py original, que continua indisponível. Os dois PDFs foram copiados de Downloads sem alteração, com igualdade de SHA-256 verificada.

## Testes e verificações

A suíte contém oito métodos de teste:

- Casos de borda: vazio, unitário, dois elementos, ordenado, invertido, todos iguais, repetidos, negativos e empates.
- Desempate obrigatório e contratos para listas sem par.
- 364 listas exaustivas de tamanhos 0 a 5, com valores -1, 0 e 1.
- 1.000 entradas aleatórias, com sementes de 1000 a 1999 e tamanhos de 2 a 80. São quatro grupos de 250 casos: sementes 1000 a 1249 usam `aleatorio` no intervalo 0 a 100; 1250 a 1499, no intervalo 0 a 1000; 1500 a 1749, no intervalo -10000 a 10000; 1750 a 1999 usam `distintos` com deslocamento e passo positivo variados, obtidos por `aleatorio` com a mesma semente. O tamanho é `2 + semente % 79`.
- A contagem efetiva encontrou 1.000 listas distintas, considerando a sequência completa de valores, e 799 resultados distintos. Houve 367 entradas com diferença mínima zero e 633 com diferença positiva. Em 582 entradas houve empate entre pelo menos dois pares de valores diferentes. A unicidade foi medida, não presumida a partir das sementes.
- Contadores em vários tamanhos e ordens, contagens conhecidas e uma entrada de 1.600 notas com semente 2026.

Um oráculo independente enumera combinações de duas posições e usa `min` para escolher por `(diferenca, menor, maior)`. Esses recursos ficam nos testes. A verificação compara o par e a diferença, confere a lista após cada chamada e compara o contador de ordenação com o mergesort da base.

Para `[4, 1, 3, 2]`, a versão ingênua conta 6 diferenças; a esperta conta 5 comparações de ordenação e 3 diferenças, total 8. O caso `[9, 9, 2, 2]` comprova que uma diferença zero não encerra os laços.

As soluções não usam sorted, list.sort, bisect, set, dict, Counter, pertencimento em listas ou min/max para encontrar o par. A base mantém seu DictWriter para exportação CSV e sorted no assert demonstrativo, conforme o material fornecido.

## Estado e próximas etapas

Concluídos: repositório Git local, cópias dos PDFs, reconstrução e validação da base, algoritmos, contadores separados, demonstrações e testes. O código é mantido em um repositório Git local, sem remoto configurado ou publicação no GitHub.

Pendentes: confirmação do professor, medições completas, análise formal de melhor e pior caso, funções misteriosas, relatório, slides e CSV definitivo. A revisão atual não implementa essas etapas.

O Codex participou da reconstrução da base, implementação, testes e documentação. A declaração completa de uso de IA será incluída no relatório acadêmico, conforme o enunciado.
