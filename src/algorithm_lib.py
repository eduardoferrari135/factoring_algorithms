import time
from sympy import factorint, nextprime

def gerar_semiprimo(bits):
    """Gera um número composto (p * q) com aproximadamente 'bits' de tamanho."""
    p = nextprime(2 ** (bits // 2))
    q = nextprime(p)
    return p * q

def benchmark_libs():
    tempo_maximo = 60
    inicio_global = time.time()
    
    bits_inicial = 20
    iteracao = 0
    maior_bits = 0
    
    print(f"--- Iniciando Benchmark com LIB (SymPy) ---")
    print(f"Tempo limite: {tempo_maximo} segundos\n")

    while True:
        tempo_atual = time.time()
        if tempo_atual - inicio_global >= tempo_maximo:
            break
            
        bits = bits_inicial + iteracao
        n = gerar_semiprimo(bits)
        
        t_inicio = time.time()
        res = factorint(n)
        t_fim = time.time()
        
        duracao = t_fim - t_inicio
        print(f"[Iteração {iteracao+1}] Bits: {n.bit_length()} | Valor: {n} | Tempo: {duracao:.5f}s")
        
        maior_bits = n.bit_length()
        iteracao += 2

    print("\n" + "="*40)
    print(f"RESULTADO FINAL (LIBS):")
    print(f"Maior tamanho alcançado: {maior_bits} bits")
    print(f"Tempo total decorrido: {time.time() - inicio_global:.2f}s")
    print("="*40)

if __name__ == "__main__":
    benchmark_libs()