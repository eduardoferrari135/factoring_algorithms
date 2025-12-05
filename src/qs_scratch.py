import time
import math
import random

def gcd(a, b):
    while b: a, b = b, a % b
    return a

def is_qrt(n, p):
    if p == 2: return True
    return pow(n, (p - 1) // 2, p) == 1

def get_primes(limit):
    """Crivo de Eratóstenes simples para gerar base"""
    primes = []
    is_prime = [True] * (limit + 1)
    for p in range(2, limit + 1):
        if is_prime[p]:
            primes.append(p)
            for i in range(p * p, limit + 1, p):
                is_prime[i] = False
    return primes

def get_factor_base(n, B):
    base = [-1]
    primes = get_primes(B)
    for p in primes:
        if is_qrt(n, p):
            base.append(p)
    return base

def gaussian_elimination(matrix):
    m = len(matrix)
    if m == 0: return []
    n_cols = len(matrix[0])
    pivot_row = [-1] * n_cols
    history = [[i] for i in range(m)]
    
    for r in range(m):
        row = matrix[r][:]
        for c in range(n_cols):
            if row[c] == 1:
                if pivot_row[c] == -1:
                    pivot_row[c] = r
                    matrix[r] = row
                    break
                else:
                    pivot_r = pivot_row[c]
                    for k in range(n_cols):
                        row[k] ^= matrix[pivot_r][k]
                    history[r].extend(history[pivot_r])
        else:
            return history[r]
    return None

def crivo_quadratico_limitado(n, timeout_start, max_duration):
    """
    Tenta fatorar n, mas aborta se o tempo global estourar.
    """
    # Parâmetros dinâmicos baseados no tamanho de bits
    bits = n.bit_length()
    if bits < 20: B, interval = 50, 1000
    elif bits < 30: B, interval = 150, 5000
    elif bits < 40: B, interval = 300, 20000
    elif bits < 50: B, interval = 700, 50000
    else: B, interval = 1500, 100000

    base = get_factor_base(n, B)
    
    root = int(math.isqrt(n))
    relations = []
    matrix = []
    
    # Busca de relações
    for i in range(interval):
        # Verifica timeout dentro do loop pesado
        if time.time() - timeout_start > max_duration:
            return None 

        x = root + i
        val = x*x - n
        original_val = val
        if val < 0: val = -val
        
        row = [0] * len(base)
        
        # Trial division (parte lenta em Python puro)
        if original_val < 0: row[0] = 1
        
        temp_val = val
        for idx, p in enumerate(base[1:], 1):
            while temp_val % p == 0:
                row[idx] ^= 1
                temp_val //= p
        
        if temp_val == 1:
            relations.append((x, original_val))
            matrix.append(row)
            
        if len(relations) > len(base) + 5:
            break
    
    if len(relations) <= len(base):
        return None # Falha: não achou relações suficientes
        
    indices = gaussian_elimination(matrix)
    if not indices: return None

    X, Y_sq = 1, 1
    for idx in indices:
        x_val, q_val = relations[idx]
        X = (X * x_val) % n
        Y_sq *= q_val
    
    Y = int(math.isqrt(Y_sq))
    f1 = gcd(abs(X - Y), n)
    
    if 1 < f1 < n:
        return f1, n // f1
    return None

def next_prime(n):
    # Função auxiliar simples para achar próximo primo
    while True:
        n += 1
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0: break
        else: return n

def gerar_semiprimo_manual(bits):
    start = 2**(bits//2)
    p = next_prime(start)
    q = next_prime(p)
    return p * q

def benchmark_scratch():
    tempo_maximo = 60
    inicio_global = time.time()
    
    bits = 15 # Começa bem menor pois Python puro é lento
    iteracao = 0
    maior_bits = 0
    
    print(f"--- Iniciando Benchmark 'DO ZERO' (Python Puro) ---")
    print("Nota: Python puro é interpretado e lento para aritmética pesada.")
    
    while True:
        if time.time() - inicio_global >= tempo_maximo:
            print("Tempo Esgotado!")
            break
            
        n = gerar_semiprimo_manual(bits)
        
        print(f"[Tentando] Bits: {n.bit_length()} | Valor: {n}...", end="", flush=True)
        
        t_inicio = time.time()
        res = crivo_quadratico_limitado(n, inicio_global, tempo_maximo)
        t_fim = time.time()
        
        if res:
            print(f" SUCESSO ({t_fim - t_inicio:.4f}s)")
            maior_bits = n.bit_length()
            bits += 2 # Aumenta 2 bits
        else:
            print(" FALHA ou TIMEOUT (tentando outro intervalo...)")
            # Se falhar, tentamos aumentar um pouco o intervalo na próxima ou abortamos se for muito grande
            if t_fim - inicio_global > tempo_maximo: break
            bits += 1 # Tenta aumentar devagar
            
        iteracao += 1

    print("\n" + "="*40)
    print(f"RESULTADO FINAL (DO ZERO):")
    print(f"Maior tamanho alcançado: {maior_bits} bits")
    print(f"Tempo total decorrido: {time.time() - inicio_global:.2f}s")
    print("="*40)

if __name__ == "__main__":
    benchmark_scratch()