"""
Gera gráfico comparando o modelo SIR com população fechada vs aberta.
"""

import numpy as np
import matplotlib.pyplot as plt
from sir_core import resolver_sir


def gerar_grafico_comparacao():
    """
    Gera um gráfico comparando os dois cenários do modelo SIR.
    """
    # Parâmetros fixos para comparação
    populacao_total = 1000
    infectados_iniciais = 1
    recuperados_iniciais = 0
    taxa_transmissao = 0.3  # β (beta)
    taxa_recuperacao = 0.1  # γ (gamma)
    
    # ========== Cenário 1: População Fechada (μ = 0) ==========
    # Sem nascimentos/mortes. A epidemia ocorre rápido e desaparece.
    dias_fechado = 200 
    tempo1, suscetiveis1, infectados1, recuperados1, r0_1 = resolver_sir(
        populacao_total, infectados_iniciais, recuperados_iniciais,
        taxa_transmissao, taxa_recuperacao, dias_fechado, taxa_vital=0.0
    )
    
    # ========== Cenário 2: População Aberta (μ > 0) ==========
    # Com nascimentos/mortes. A doença oscila até um equilíbrio endêmico.
    dias_aberto = 1000
    taxa_vital = 0.01  # μ (mu) - valor alto para efeito didático
    tempo2, suscetiveis2, infectados2, recuperados2, r0_2 = resolver_sir(
        populacao_total, infectados_iniciais, recuperados_iniciais,
        taxa_transmissao, taxa_recuperacao, dias_aberto, taxa_vital=taxa_vital
    )

    # ========== Criar a figura com dois gráficos lado a lado ==========
    figura, (eixo1, eixo2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Gráfico 1: População Fechada
    eixo1.plot(tempo1, suscetiveis1, 'b', label='Suscetíveis')
    eixo1.plot(tempo1, infectados1, 'r', label='Infectados')
    eixo1.plot(tempo1, recuperados1, 'g', label='Recuperados')
    eixo1.set_title(f'População Fechada ($\\mu=0$)\n$R_0={r0_1:.2f}$ (Epidemia única)')
    eixo1.set_xlabel('Tempo (dias)')
    eixo1.set_ylabel('População')
    eixo1.legend()
    eixo1.grid(True, alpha=0.3)
    
    # Gráfico 2: População Aberta
    eixo2.plot(tempo2, suscetiveis2, 'b', label='Suscetíveis')
    eixo2.plot(tempo2, infectados2, 'r', label='Infectados')
    eixo2.plot(tempo2, recuperados2, 'g', label='Recuperados')
    
    # Linha do equilíbrio endêmico teórico para I*
    if r0_2 > 1:
        infectados_equilibrio = (taxa_vital * populacao_total / taxa_transmissao) * (r0_2 - 1)
        eixo2.axhline(y=infectados_equilibrio, color='r', linestyle='--', alpha=0.5, 
                      label=f'Equilíbrio I*={infectados_equilibrio:.1f}')

    eixo2.set_title(f'População Aberta ($\\mu={taxa_vital}$)\n$R_0={r0_2:.2f}$ (Endemia oscilatória)')
    eixo2.set_xlabel('Tempo (dias)')
    eixo2.legend()
    eixo2.grid(True, alpha=0.3)

    # Salvar figura
    plt.tight_layout()
    plt.savefig('comparacao_sir.png', dpi=300)
    print("Gráfico salvo como 'comparacao_sir.png'")


if __name__ == "__main__":
    gerar_grafico_comparacao()

