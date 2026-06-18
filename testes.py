from controlador import TriangularMF, TrapezoidalMF, VariavelFuzzy, RegraFuzzy, ControladorFuzzy

def test_triangular_mf():
    print("Executando test_triangular_mf...")
    # média: Triângulo de 900 a 1100, pico em 1000
    mf = TriangularMF(900.0, 1000.0, 1100.0)
    assert mf.calcular(900.0) == 0.0, f"Falha em 900: {mf.calcular(900.0)}"
    assert mf.calcular(950.0) == 0.5, f"Falha em 950: {mf.calcular(950.0)}"
    assert mf.calcular(1000.0) == 1.0, f"Falha em 1000: {mf.calcular(1000.0)}"
    assert mf.calcular(1050.0) == 0.5, f"Falha em 1050: {mf.calcular(1050.0)}"
    assert mf.calcular(1100.0) == 0.0, f"Falha em 1100: {mf.calcular(1100.0)}"
    assert mf.calcular(800.0) == 0.0, f"Falha em 800: {mf.calcular(800.0)}"
    assert mf.calcular(1200.0) == 0.0, f"Falha em 1200: {mf.calcular(1200.0)}"
    print("test_triangular_mf passou!")

def test_trapezoidal_mf_left():
    print("Executando test_trapezoidal_mf_left (baixa)...")
    # baixa: Trapézio estável em 1 de 800 a 900, decai até 1000
    mf = TrapezoidalMF(800.0, 800.0, 900.0, 1000.0)
    assert mf.calcular(800.0) == 1.0, f"Falha em 800: {mf.calcular(800.0)}"
    assert mf.calcular(850.0) == 1.0, f"Falha em 850: {mf.calcular(850.0)}"
    assert mf.calcular(900.0) == 1.0, f"Falha em 900: {mf.calcular(900.0)}"
    assert mf.calcular(950.0) == 0.5, f"Falha em 950: {mf.calcular(950.0)}"
    assert mf.calcular(1000.0) == 0.0, f"Falha em 1000: {mf.calcular(1000.0)}"
    assert mf.calcular(750.0) == 1.0, f"Falha em 750: {mf.calcular(750.0)}"
    assert mf.calcular(1100.0) == 0.0, f"Falha em 1100: {mf.calcular(1100.0)}"
    print("test_trapezoidal_mf_left passou!")

def test_trapezoidal_mf_right():
    print("Executando test_trapezoidal_mf_right (alta)...")
    # alta: Trapézio subindo em 1000, 1 em 1100, estável até 1200
    mf = TrapezoidalMF(1000.0, 1100.0, 1200.0, 1200.0)
    assert mf.calcular(950.0) == 0.0, f"Falha em 950: {mf.calcular(950.0)}"
    assert mf.calcular(1000.0) == 0.0, f"Falha em 1000: {mf.calcular(1000.0)}"
    assert mf.calcular(1050.0) == 0.5, f"Falha em 1050: {mf.calcular(1050.0)}"
    assert mf.calcular(1100.0) == 1.0, f"Falha em 1100: {mf.calcular(1100.0)}"
    assert mf.calcular(1150.0) == 1.0, f"Falha em 1150: {mf.calcular(1150.0)}"
    assert mf.calcular(1200.0) == 1.0, f"Falha em 1200: {mf.calcular(1200.0)}"
    assert mf.calcular(1250.0) == 1.0, f"Falha em 1250: {mf.calcular(1250.0)}"
    print("test_trapezoidal_mf_right passou!")

def test_variavel_fuzzy():
    print("Executando test_variavel_fuzzy...")
    v = VariavelFuzzy("Temperatura", 800.0, 1200.0)
    v.adicionar_termo("baixa", TrapezoidalMF(800.0, 800.0, 900.0, 1000.0))
    v.adicionar_termo("media", TriangularMF(900.0, 1000.0, 1100.0))
    v.adicionar_termo("alta", TrapezoidalMF(1000.0, 1100.0, 1200.0, 1200.0))

    # Testando com valor no meio da rampa de baixa
    pert = v.fuzzificar(950.0)
    assert pert["baixa"] == 0.5, f"baixa em 950: {pert['baixa']}"
    assert pert["media"] == 0.5, f"media em 950: {pert['media']}"
    assert pert["alta"] == 0.0, f"alta em 950: {pert['alta']}"

    # Testando fora do limite superior (clamping)
    pert_fora = v.fuzzificar(1250.0)
    assert pert_fora["alta"] == 1.0, f"alta em 1250: {pert_fora['alta']}"
    assert pert_fora["baixa"] == 0.0, f"baixa em 1250: {pert_fora['baixa']}"
    print("test_variavel_fuzzy passou!")

if __name__ == "__main__":
    test_triangular_mf()
    test_trapezoidal_mf_left()
    test_trapezoidal_mf_right()
    test_variavel_fuzzy()
    print("Todos os testes passaram com sucesso!")
