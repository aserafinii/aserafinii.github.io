def obter_parametros_usuario():
    """
    Solicita os parâmetros da simulação ao usuário via terminal.
    Retorna valores padrão se o usuário apenas pressionar Enter.
    """
    print("Dá Enter para usar o valor padrão.\n")

    def obter_entrada(prompt, padrao, tipo=float):
        try:
            valor = input(f"{prompt} [{padrao}]: ").strip()
            if not valor:
                return padrao
            return tipo(valor)
        except ValueError:
            print(f"Valor inválido. Usando padrão: {padrao}")
            return padrao

    populacao_total = obter_entrada("População Total (N)", 1000, int)
    infectados_iniciais = obter_entrada("Infectados Iniciais (I0)", 1, int)
    recuperados_iniciais = obter_entrada("Recuperados Iniciais (R0)", 0, int)
    dias_simulacao = obter_entrada("Dias de Simulação", 365, int)
    
    print("\n--- Parâmetros da Doença ---")
    taxa_transmissao = obter_entrada("Taxa de Transmissão (0.3)", 0.3, float)
    taxa_recuperacao = obter_entrada("Taxa de Recuperação (0.1)", 0.1, float)
    
    print("\n--- Parâmetros Demográficos (Opcional) ---")
    print("Use 0 para população fechada (sem nascimentos/mortes).")
    taxa_vital = obter_entrada("Taxa de natalidade/mortalidade (mu) (ex: 0.01)", 0.0, float)

    return populacao_total, infectados_iniciais, recuperados_iniciais, taxa_transmissao, taxa_recuperacao, dias_simulacao, taxa_vital


# Alias para compatibilidade
def get_user_params():
    """Wrapper para manter compatibilidade com código existente."""
    return obter_parametros_usuario()
