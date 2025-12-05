import time
import math
import random

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def pollard_rho_limitado(n, timeout_start, max_duration):
    """
    Implementação do Pollard's Rho (Algoritmo do Canguru).
    Retorna um fator não trivial de n ou None se falhar/timeout.
    """
    if n % 2 == 0:
        return 2
        
    # O Pollard's rho é probabilístico. 
    # Tenta com c=1. Se falhar, loops externos poderiam tentar outros c,
    # mas para este benchmark manteremos simples.
    x = 2
    y = 2
    d = 1
    c = 1
    
    cycle_check = 0
    
    f = lambda x: (x * x + c) % n

    while d == 1:
        x = f(x)
        
        y = f(f(y))
        
        d = gcd(abs(x - y), n)
        
        cycle_check += 1
        if cycle_check % 10000 == 0:
            if time.time() - timeout_start > max_duration:
                return None # Timeout forçado

    if d == n:
        return None 
    
    return d 


def next_prime(n):
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

def benchmark_pollard():
    tempo_maximo = 60
    inicio_global = time.time()
    
    # Começamos igual ao QS para comparação justa
    bits = 15 
    iteracao = 0
    maior_bits = 0
    
    print(f"--- Iniciando Benchmark 'POLLARD'S RHO' (Python Puro) ---")
    
    while True:
        if time.time() - inicio_global >= tempo_maximo:
            print("Tempo Esgotado!")
            break
            
        n = gerar_semiprimo_manual(bits)
        
        print(f"[Tentando] Bits: {n.bit_length()} | Valor: {n}...", end="", flush=True)
        
        t_inicio = time.time()
        # Passamos o tempo global para ele abortar se estourar o minuto no meio do calculo
        fator = pollard_rho_limitado(n, inicio_global, tempo_maximo)
        t_fim = time.time()
        
        duracao = t_fim - t_inicio
        
        if fator:
            print(f" SUCESSO ({duracao:.5f}s)")
            maior_bits = n.bit_length()
            bits += 2 # Aumenta 2 bits a cada sucesso
        else:
            print(" TIMEOUT ou FALHA")
            break # Se falhar no Pollard normalmente é porque o número ficou grande demais para o tempo
            
        iteracao += 1

    print("\n" + "="*40)
    print(f"RESULTADO FINAL (POLLARD DO ZERO):")
    print(f"Maior tamanho alcançado: {maior_bits} bits")
    print(f"Tempo total decorrido: {time.time() - inicio_global:.2f}s")
    print("="*40)

if __name__ == "__main__":
    benchmark_pollard()