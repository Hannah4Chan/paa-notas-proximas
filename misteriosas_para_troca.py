def misteriosa_a(n):
    """Recebe um inteiro n >= 0 e devolve o resultado."""
    resultado = 0
    for i in range(n):
        for j in range(7):
            resultado += i  # ←
    return resultado


def misteriosa_b(n):
    """Recebe um inteiro n >= 0 e devolve o resultado."""
    resultado = 0
    i = 1
    while i <= n:
        resultado += i  # ←
        i *= 3
    return resultado
