## Comparativo de Performance

Este projeto compara três abordagens distintas de fatoração de inteiros:
1.  **Crivo Quadrático (QS):** Implementação didática "Do Zero" em Python.
2.  **Pollard's Rho:** Implementação didática "Do Zero" em Python.
3.  **SymPy:** Biblioteca profissional que utiliza implementações otimizadas em C (GMP, ECM, GNFS).

### Resumo dos Resultados (Benchmark de 60 segundos)

| Característica | Crivo Quadrático (Python) | Pollard's Rho (Python) | Lib Profissional (SymPy) |
| :--- | :--- | :--- | :--- |
| **Complexidade** | Alta (Matrizes, Peneira) | Baixa (Aritmética Simples) | Otimizada / Híbrida |
| **Execução** | Interpretada (Lenta) | Interpretada (Média) | Compilada em C (Rápida) |
| **Maior Fatorado** | **61 bits** (~18 dígitos) | **93 bits** (~28 dígitos) | **1647 bits** (~496 dígitos) |
| **Desempenho** | Falha rápido devido ao overhead | Bom para números médios | Escala exponencialmente |

### Comparação Direta de Tempos

Abaixo, comparamos o tempo necessário para fatorar números de tamanhos idênticos em cada implementação.

| Tamanho | Valor (Semiprimo) | Tempo QS (Python) | Tempo Rho (Python) | Tempo SymPy (Lib) | Observação |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **21 bits** | `1065023` | 0.00060s | **0.00001s** | 0.00003s | Rho vence (menos overhead) |
| **41 bits** | `1099532599387` | 0.00720s | 0.00101s | **0.00010s** | Lib assume a liderança |
| **51 bits** | `1125902456980891` | 0.05030s | 0.00319s | **0.00014s** | Rho é ~15x mais rápido que QS |
| **61 bits** | `1152921515344265237` | 0.43760s | 0.03774s | **0.00016s** | QS começa a engasgar |
| **67 bits** | `73786976689975198189` | *TIMEOUT* ❌ | 0.05165s | **0.00018s** | QS atinge o limite |
| **93 bits** | `495176... (28 dígitos)` | --- | 21.93s | **< 0.001s** | Rho atinge o limite |
| **1647 bits** | `(Número de ~496 dígitos)` | --- | --- | **< 60s** | Domínio total da Lib |

> **Conclusão:** > 1. **Pollard's Rho vs QS (Python):** O Pollard's Rho é muito mais eficiente que o Crivo Quadrático para implementações em Python puro nesta faixa de bits, pois não possui o overhead de gerenciamento de memória e matrizes do Crivo.
> 2. **Python vs Libs:** Mesmo o melhor algoritmo em Python puro (Rho) não consegue competir com bibliotecas otimizadas em C (SymPy) assim que os números passam de 40 bits. A Lib processou números com centenas de dígitos enquanto o Python lutava com 28 dígitos.