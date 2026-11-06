def misteriosa_a(n):
    """Recebe um inteiro n >= 0 e devolve (resultado, contagem)."""
    resultado = 0
    contagem = 0
    for i in range(n):
        for j in range(7):
            resultado += i  # ←
            contagem += 1
    return resultado, contagem


def misteriosa_b(n):
    """Recebe um inteiro n >= 0 e devolve (resultado, contagem)."""
    resultado = 0
    contagem = 0
    i = 1
    while i <= n:
        resultado += i  # ←
        contagem += 1
        i *= 3
    return resultado, contagem
