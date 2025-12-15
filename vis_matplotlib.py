import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from sir_core import solve_sir
from utils import get_user_params


def executar_animacao_matplotlib():
    """
    Executa uma animação do modelo SIR usando Matplotlib.
    """
    # Obter parâmetros do usuário
    (populacao_total, infectados_iniciais, recuperados_iniciais, 
     taxa_transmissao, taxa_recuperacao, dias_simulacao, taxa_vital) = obter_parametros_usuario()

    # Resolver o modelo
    tempo, suscetiveis, infectados, recuperados, r0 = resolver_sir(
        populacao_total, infectados_iniciais, recuperados_iniciais,
        taxa_transmissao, taxa_recuperacao, dias_simulacao, taxa_vital
    )

    # Configuração do Plot
    figura, eixo = plt.subplots(figsize=(10, 6))
    eixo.set_xlim(0, dias_simulacao)
    eixo.set_ylim(0, populacao_total)
    eixo.set_xlabel('Tempo (dias)')
    eixo.set_ylabel('População')
    
    sufixo_titulo = " (Pop. Aberta)" if taxa_vital > 0 else ""
    eixo.set_title(f'Modelo SIR{sufixo_titulo} (N={populacao_total})')
    
    # Linhas vazias para iniciar
    linha_s, = eixo.plot([], [], 'b-', label='Suscetíveis', linewidth=2)
    linha_i, = eixo.plot([], [], 'r-', label='Infectados', linewidth=2)
    linha_r, = eixo.plot([], [], 'g-', label='Recuperados', linewidth=2)
    
    eixo.legend()
    eixo.grid(True, alpha=0.3)

    def inicializar():
        linha_s.set_data([], [])
        linha_i.set_data([], [])
        linha_r.set_data([], [])
        return linha_s, linha_i, linha_r

    def atualizar(frame):
        tempo_atual = tempo[:frame]
        suscetiveis_atual = suscetiveis[:frame]
        infectados_atual = infectados[:frame]
        recuperados_atual = recuperados[:frame]
        
        linha_s.set_data(tempo_atual, suscetiveis_atual)
        linha_i.set_data(tempo_atual, infectados_atual)
        linha_r.set_data(tempo_atual, recuperados_atual)
        
        return linha_s, linha_i, linha_r

    animacao = FuncAnimation(
        figura, atualizar, 
        frames=range(1, len(tempo)+1, 2),  # Pula frames para velocidade
        init_func=inicializar, 
        blit=True, 
        interval=30
    )
    
    print("Gerando animação Matplotlib...")
    plt.show()


if __name__ == "__main__":
    executar_animacao_matplotlib()
