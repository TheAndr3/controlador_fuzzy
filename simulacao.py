import os
import numpy as np
import matplotlib.pyplot as plt
from controlador import (
    TriangularMF,
    TrapezoidalMF,
    VariavelFuzzy,
    RegraFuzzy,
    ControladorFuzzy
)

def criar_sistema_fuzzy() -> ControladorFuzzy:
    """Configura o sistema fuzzy de caldeira conforme o escopo do projeto."""
    controlador = ControladorFuzzy(num_pontos=500)

    # 1. Configurando Variáveis de Entrada
    
    # Temperatura: 800 a 1200 °C
    t_var = VariavelFuzzy("Temperatura", 800.0, 1200.0)
    t_var.adicionar_termo("baixa", TrapezoidalMF(800.0, 800.0, 900.0, 1000.0))
    t_var.adicionar_termo("media", TriangularMF(900.0, 1000.0, 1100.0))
    t_var.adicionar_termo("alta", TrapezoidalMF(1000.0, 1100.0, 1200.0, 1200.0))
    controlador.adicionar_variable_entrada = t_var # Wait, we have a method adicionar_variavel_entrada in controlador.py
    # let's double check if we call the correct method
    controlador.adicionar_variavel_entrada(t_var)

    # Volume: 2 a 12 m³
    v_var = VariavelFuzzy("Volume", 2.0, 12.0)
    v_var.adicionar_termo("pequeno", TrapezoidalMF(2.0, 2.0, 4.5, 7.0))
    v_var.adicionar_termo("medio", TriangularMF(4.5, 7.0, 9.5))
    v_var.adicionar_termo("grande", TrapezoidalMF(7.0, 9.5, 12.0, 12.0))
    controlador.adicionar_variavel_entrada(v_var)

    # 2. Configurando Variável de Saída
    
    # Pressão: 4 a 12 atm
    p_var = VariavelFuzzy("Pressão", 4.0, 12.0)
    p_var.adicionar_termo("baixa", TrapezoidalMF(4.0, 4.0, 5.0, 8.0))
    p_var.adicionar_termo("media", TriangularMF(6.0, 8.0, 10.0))
    p_var.adicionar_termo("alta", TrapezoidalMF(8.0, 11.0, 12.0, 12.0))
    controlador.adicionar_variavel_saida(p_var)

    # 3. Configurando as Regras Fuzzy
    
    # R1: Se (T é Baixa) e (V é Pequeno) Então (P é Baixa)
    controlador.adicionar_regra(RegraFuzzy({"Temperatura": "baixa", "Volume": "pequeno"}, ("Pressão", "baixa")))
    # R2: Se (T é Média) e (V é Pequeno) Então (P é Baixa)
    controlador.adicionar_regra(RegraFuzzy({"Temperatura": "media", "Volume": "pequeno"}, ("Pressão", "baixa")))
    # R3: Se (T é Alta) e (V é Pequeno) Então (P é Média)
    controlador.adicionar_regra(RegraFuzzy({"Temperatura": "alta", "Volume": "pequeno"}, ("Pressão", "media")))
    # R4: Se (T é Baixa) e (V é Médio) Então (P é Baixa)
    controlador.adicionar_regra(RegraFuzzy({"Temperatura": "baixa", "Volume": "medio"}, ("Pressão", "baixa")))
    # R5: Se (T é Média) e (V é Médio) Então (P é Média)
    controlador.adicionar_regra(RegraFuzzy({"Temperatura": "media", "Volume": "medio"}, ("Pressão", "media")))
    # R6: Se (T é Alta) e (V é Médio) Então (P é Alta)
    controlador.adicionar_regra(RegraFuzzy({"Temperatura": "alta", "Volume": "medio"}, ("Pressão", "alta")))
    # R7: Se (T é Baixa) e (V é Grande) Então (P é Média)
    controlador.adicionar_regra(RegraFuzzy({"Temperatura": "baixa", "Volume": "grande"}, ("Pressão", "media")))
    # R8: Se (T é Média) e (V é Grande) Então (P é Alta)
    controlador.adicionar_regra(RegraFuzzy({"Temperatura": "media", "Volume": "grande"}, ("Pressão", "alta")))
    # R9: Se (T é Alta) e (V é Grande) Então (P é Alta)
    controlador.adicionar_regra(RegraFuzzy({"Temperatura": "alta", "Volume": "grande"}, ("Pressão", "alta")))

    return controlador

def plotar_funcoes_pertinencia(controlador: ControladorFuzzy, output_dir: str):
    """Gera um gráfico geral mostrando todas as funções de pertinência do sistema."""
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10))

    # Temperatura
    t_var = controlador.variaveis_entrada["Temperatura"]
    x_t = np.linspace(t_var.min_val, t_var.max_val, 500)
    for termo, mf in t_var.termos.items():
        y = [mf.calcular(val) for val in x_t]
        ax1.plot(x_t, y, label=termo, linewidth=2)
    ax1.set_title("Funções de Pertinência da Temperatura")
    ax1.set_xlabel("Temperatura (°C)")
    ax1.set_ylabel("Pertinência")
    ax1.grid(True, linestyle="--", alpha=0.6)
    ax1.legend()

    # Volume
    v_var = controlador.variaveis_entrada["Volume"]
    x_v = np.linspace(v_var.min_val, v_var.max_val, 500)
    for termo, mf in v_var.termos.items():
        y = [mf.calcular(val) for val in x_v]
        ax2.plot(x_v, y, label=termo, linewidth=2)
    ax2.set_title("Funções de Pertinência do Volume")
    ax2.set_xlabel("Volume (m³)")
    ax2.set_ylabel("Pertinência")
    ax2.grid(True, linestyle="--", alpha=0.6)
    ax2.legend()

    # Pressão
    p_var = controlador.variaveis_saida["Pressão"]
    x_p = np.linspace(p_var.min_val, p_var.max_val, 500)
    for termo, mf in p_var.termos.items():
        y = [mf.calcular(val) for val in x_p]
        ax3.plot(x_p, y, label=termo, linewidth=2)
    ax3.set_title("Funções de Pertinência da Pressão (Saída)")
    ax3.set_xlabel("Pressão (atm)")
    ax3.set_ylabel("Pertinência")
    ax3.grid(True, linestyle="--", alpha=0.6)
    ax3.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "funcoes_pertinencia.png"), dpi=150)
    plt.close()

def executar_e_salvar_simulacao(controlador: ControladorFuzzy, caso_letra: str, temp: float, vol: float, output_dir: str):
    """Simula um caso específico, exibe no terminal e gera os gráficos correspondentes."""
    entradas = {"Temperatura": temp, "Volume": vol}
    res = controlador.simular(entradas, "Pressão")
    defuzificado, universo_saida, pert_agregada, valores_fuzzificados, ativacoes_regras, regioes_regras = res

    # Imprimir resultado no terminal
    print(f"\n==================================================")
    print(f" CASO {caso_letra.upper()} | Temperatura = {temp}°C | Volume = {vol} m³")
    print(f"==================================================")
    
    print("Fuzificação das Entradas:")
    print(" - Temperatura:")
    for termo, grau in valores_fuzzificados["Temperatura"].items():
        print(f"    * {termo}: {grau:.4f}")
    print(" - Volume:")
    for termo, grau in valores_fuzzificados["Volume"].items():
        print(f"    * {termo}: {grau:.4f}")

    print("\nAtivação das Regras:")
    for i, regra in enumerate(controlador.regras):
        desc = " E ".join([f"({k} é {v})" for k, v in regra.antecedentes.items()])
        conseq = f"({regra.consequente_var} é {regra.consequente_termo})"
        alfa = ativacoes_regras[i]
        print(f"  Regra {i+1}: Se {desc} Então {conseq} | Ativação (alfa) = {alfa:.4f}")

    print(f"\nValor Desfuzificado (Centróide): Pressão = {defuzificado:.4f} atm")

    # Plotar região fuzzy de saída do caso
    p_var = controlador.variaveis_saida["Pressão"]
    plt.figure(figsize=(9, 5))

    # Desenhar as curvas originais de pertinência da Pressão como referência
    for termo, mf in p_var.termos.items():
        y = [mf.calcular(val) for val in universo_saida]
        plt.plot(universo_saida, y, '--', color='gray', alpha=0.5, label=f'_ref_{termo}')

    # Plotar região preenchida agregada
    plt.plot(universo_saida, pert_agregada, 'r-', linewidth=2.5, label='Região Fuzzy Agregada')
    plt.fill_between(universo_saida, 0, pert_agregada, color='red', alpha=0.25)

    # Plotar a linha do Centróide
    plt.axvline(x=defuzificado, color='blue', linestyle='--', linewidth=2, 
                label=f'Centróide = {defuzificado:.4f} atm')

    # Anotações adicionais no gráfico
    plt.title(f'Região Fuzzy de Saída - Caso {caso_letra.upper()}\n(Temp = {temp}°C, Volume = {vol}m³)')
    plt.xlabel('Pressão (atm)')
    plt.ylabel('Grau de Pertinência')
    plt.xlim(p_var.min_val - 0.5, p_var.max_val + 0.5)
    plt.ylim(-0.05, 1.05)
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend(loc='upper right')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"caso_{caso_letra}.png"), dpi=150)
    plt.close()

def main():
    # Garantir que o diretório de gráficos exista
    output_dir = "graficos"
    os.makedirs(output_dir, exist_ok=True)

    print("Configurando o sistema fuzzy...")
    controlador = criar_sistema_fuzzy()

    print("Gerando gráficos das funções de pertinência gerais...")
    plotar_funcoes_pertinencia(controlador, output_dir)
    print(f"Gráfico geral salvo em: {os.path.join(output_dir, 'funcoes_pertinencia.png')}")

    # Lista de Casos de Teste para Simulação
    # a) Temp = 965°C e Volume = 11m³
    # b) Temp = 920°C e Volume = 7.6m³
    # c) Temp = 1050°C e Volume = 6.3m³
    # d) Temp = 843°C e Volume = 8.6m³
    # e) Temp = 1122°C e Volume = 5.2m³
    casos = [
        ("a", 965.0, 11.0),
        ("b", 920.0, 7.6),
        ("c", 1050.0, 6.3),
        ("d", 843.0, 8.6),
        ("e", 1122.0, 5.2),
    ]

    for letra, temp, vol in casos:
        executar_e_salvar_simulacao(controlador, letra, temp, vol, output_dir)

    print("\nSimulação concluída com sucesso! Todos os gráficos foram salvos na pasta 'graficos/'.")

if __name__ == "__main__":
    main()
