import numpy as np

class FuncaoPertinencia:
    """Classe base abstrata para representar funções de pertinência fuzzy."""
    def calcular(self, x: float) -> float:
        raise NotImplementedError("O método calcular deve ser implementado pelas subclasses.")

class TriangularMF(FuncaoPertinencia):
    """Função de pertinência triangular definida por três pontos: a, b e c (com a <= b <= c)."""
    def __init__(self, a: float, b: float, c: float):
        self.a = a
        self.b = b
        self.c = c

    def calcular(self, x: float) -> float:
        if x <= self.a or x >= self.c:
            return 0.0
        if x == self.b:
            return 1.0
        if self.a < x < self.b:
            return (x - self.a) / (self.b - self.a) if self.b != self.a else 1.0
        if self.b < x < self.c:
            return (self.c - x) / (self.c - self.b) if self.c != self.b else 1.0
        return 0.0

class TrapezoidalMF(FuncaoPertinencia):
    """Função de pertinência trapezoidal definida por quatro pontos: a, b, c e d (com a <= b <= c <= d)."""
    def __init__(self, a: float, b: float, c: float, d: float):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def calcular(self, x: float) -> float:
        # Trata o limite esquerdo se for plano infinito à esquerda (a == b)
        if self.a == self.b and x <= self.a:
            return 1.0
        # Trata o limite direito se for plano infinito à direita (c == d)
        if self.c == self.d and x >= self.d:
            return 1.0

        if x <= self.a or x >= self.d:
            return 0.0
        if self.b <= x <= self.c:
            return 1.0
        if self.a < x < self.b:
            return (x - self.a) / (self.b - self.a) if self.b != self.a else 1.0
        if self.c < x < self.d:
            return (self.d - x) / (self.d - self.c) if self.d != self.c else 1.0
        return 0.0

class VariavelFuzzy:
    """Representa uma variável linguística fuzzy, com seu universo de discurso e conjuntos fuzzy."""
    def __init__(self, nome: str, min_val: float, max_val: float):
        self.nome = nome
        self.min_val = min_val
        self.max_val = max_val
        self.termos = {}  # Mapeia nome_termo -> FuncaoPertinencia

    def adicionar_termo(self, nome_termo: str, funcao: FuncaoPertinencia):
        self.termos[nome_termo] = funcao

    def fuzzificar(self, valor: float) -> dict:
        # Clampa o valor de entrada para o universo de discurso
        valor_clamped = max(self.min_val, min(self.max_val, valor))
        res = {}
        for nome_termo, funcao in self.termos.items():
            res[nome_termo] = funcao.calcular(valor_clamped)
        return res

class RegraFuzzy:
    """Representa uma regra fuzzy no formato: Se (Var1 é Termo1) e (Var2 é Termo2) Então (VarSaida é TermoSaida)."""
    def __init__(self, antecedentes: dict, consequente: tuple):
        # antecedentes: dict do tipo {"NomeVariavel": "NomeTermo"}
        # consequente: tuple do tipo ("NomeVariavelSaida", "NomeTermoSaida")
        self.antecedentes = antecedentes
        self.consequente_var, self.consequente_termo = consequente

    def avaliar_antecedente(self, valores_fuzzificados: dict) -> float:
        # Calcula o nível de ativação alpha usando operador E (mínimo)
        graus = []
        for var_nome, termo_nome in self.antecedentes.items():
            grau = valores_fuzzificados.get(var_nome, {}).get(termo_nome, 0.0)
            graus.append(grau)
        return min(graus) if graus else 0.0

class ControladorFuzzy:
    """Motor de Inferência Fuzzy Mamdani que gerencia variáveis, regras e executa a inferência."""
    def __init__(self, num_pontos: int = 500):
        self.num_pontos = num_pontos
        self.variaveis_entrada = {}
        self.variaveis_saida = {}
        self.regras = []

    def adicionar_variavel_entrada(self, var: VariavelFuzzy):
        self.variaveis_entrada[var.nome] = var

    def adicionar_variavel_saida(self, var: VariavelFuzzy):
        self.variaveis_saida[var.nome] = var

    def adicionar_regra(self, regra: RegraFuzzy):
        self.regras.append(regra)

    def simular(self, entradas: dict, var_saida_nome: str) -> tuple:
        """
        Executa a simulação fuzzy para um conjunto de valores crisp de entrada.
        Retorna:
            - valor_desfuzificado (float)
            - universo_saida (np.ndarray)
            - pertinencia_agregada (np.ndarray)
            - valores_fuzzificados (dict)
            - ativacoes_regras (list of float)
            - regioes_regras (list of np.ndarray)
        """
        # 1. Fuzzificação
        valores_fuzzificados = {}
        for nome, valor in entradas.items():
            var = self.variaveis_entrada[nome]
            valores_fuzzificados[nome] = var.fuzzificar(valor)

        # 2. Obter universo discretizado da variável de saída
        var_saida = self.variaveis_saida[var_saida_nome]
        universo_saida = np.linspace(var_saida.min_val, var_saida.max_val, self.num_pontos)

        # 3. Inferência de cada regra e Agregação
        pertinencia_agregada = np.zeros(self.num_pontos)
        ativacoes_regras = []
        regioes_regras = []

        for regra in self.regras:
            alfa = regra.avaliar_antecedente(valores_fuzzificados)
            ativacoes_regras.append(alfa)

            # Obter a função de pertinência do termo do consequente
            consequente_funcao = var_saida.termos[regra.consequente_termo]
            
            # Calcular pertinência para todo o universo discretizado
            pert_consequente = np.array([consequente_funcao.calcular(z) for z in universo_saida])
            
            # Aplicar implicação (mínimo)
            regiao_regra = np.minimum(alfa, pert_consequente)
            regioes_regras.append(regiao_regra)

            # Agregar usando operador união (máximo)
            pertinencia_agregada = np.maximum(pertinencia_agregada, regiao_regra)

        # 4. Desfuzificação pelo Centro de Área (Centróide)
        soma_pertinencias = np.sum(pertinencia_agregada)
        if soma_pertinencias == 0.0:
            # Caso nenhuma regra seja ativada, retorna o centro geométrico do universo
            defuzificado = (var_saida.min_val + var_saida.max_val) / 2.0
        else:
            defuzificado = np.sum(universo_saida * pertinencia_agregada) / soma_pertinencias

        return defuzificado, universo_saida, pertinencia_agregada, valores_fuzzificados, ativacoes_regras, regioes_regras
