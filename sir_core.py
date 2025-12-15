"""
Núcleo do modelo SIR com dinâmica vital.

Este módulo resolve numericamente o sistema de EDOs do modelo SIR
usando o método Runge-Kutta do SciPy.
"""

import numpy as np
from scipy.integrate import solve_ivp


def derivadas_sir(tempo, estado, populacao_total, taxa_transmissao, taxa_recuperacao, taxa_vital):
    """
    Calcula as derivadas do sistema SIR com dinâmica vital.
    
    Retorna [dS/dt, dI/dt, dR/dt] dado o estado atual.
    """
    suscetiveis, infectados, recuperados = estado
    
    # Força de infecção (λ = β * I / N)
    forca_infeccao = taxa_transmissao * infectados / populacao_total
    
    # Derivadas do sistema SIR
    dS_dt = taxa_vital * populacao_total - forca_infeccao * suscetiveis - taxa_vital * suscetiveis
    dI_dt = forca_infeccao * suscetiveis - taxa_recuperacao * infectados - taxa_vital * infectados
    dR_dt = taxa_recuperacao * infectados - taxa_vital * recuperados
    
    return [dS_dt, dI_dt, dR_dt]


def calcular_r0(taxa_transmissao, taxa_recuperacao, taxa_vital):
    """
    Calcula o número básico de reprodução R₀.
    
    R₀ = β / (γ + μ)
    """
    return taxa_transmissao / (taxa_recuperacao + taxa_vital)


def resolver_sir(populacao_total, infectados_iniciais, recuperados_iniciais, 
                 taxa_transmissao, taxa_recuperacao, dias, taxa_vital=0.0):
    """
    Resolve o modelo SIR numericamente usando Runge-Kutta do SciPy.
    
    Parâmetros:
        populacao_total: N - população total
        infectados_iniciais: I₀ - número inicial de infectados
        recuperados_iniciais: R₀ - número inicial de recuperados
        taxa_transmissao: β (beta)
        taxa_recuperacao: γ (gamma)
        dias: duração da simulação
        taxa_vital: μ (mu) - taxa de natalidade/mortalidade
    
    Retorna:
        tempo, suscetiveis, infectados, recuperados, r0
    """
    # Condições iniciais
    suscetiveis_inicial = populacao_total - infectados_iniciais - recuperados_iniciais
    estado_inicial = [suscetiveis_inicial, infectados_iniciais, recuperados_iniciais]
    
    # Intervalo de tempo e pontos onde queremos a solução
    intervalo = (0, dias)
    pontos_tempo = np.linspace(0, dias, dias + 1)
    
    # Resolver usando Runge-Kutta do SciPy
    solucao = solve_ivp(
        derivadas_sir,
        intervalo,
        estado_inicial,
        method='RK45',
        t_eval=pontos_tempo,
        args=(populacao_total, taxa_transmissao, taxa_recuperacao, taxa_vital)
    )
    
    # Extrair resultados
    tempo = solucao.t
    suscetiveis = solucao.y[0]
    infectados = solucao.y[1]
    recuperados = solucao.y[2]
    
    # Calcular R₀
    r0 = calcular_r0(taxa_transmissao, taxa_recuperacao, taxa_vital)
    
    return tempo, suscetiveis, infectados, recuperados, r0
