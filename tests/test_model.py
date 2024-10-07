from services.model_service import Model

def test_build_context():
    analitics = {
        'best_p': ('Prueba', 100),
        'old_eff_d': ('01-01-2020', 'Document A'),
        'new_eff_d': ('01-01-2021', 'Document B'),
        'short_rt': 1,
        'long_rt': 365
    }
    model = Model(analitics)
    expected = """
                El proveedor más popular es Prueba porque tiene 100.\n
                La fecha efectiva más reciente es 01-01-2021 del contrato Document B.\n
                El plazo de renovación más corto es 1 días.\n
                El plazo de renovación más extenso es 365 días.\n
                La fecha efectiva más antigua es 01-01-2020.
                """
    assert model.context == expected

def test_ask_question():
    analitics = {
        'best_p': ('Prueba', 100),
        'old_eff_d': ('01-01-2020', 'Document A'),
        'new_eff_d': ('01-01-2021', 'Document B'),
        'short_rt': 1,
        'long_rt': 365
    }
    model = Model(analitics)
    question = '¿Quién es el proveedor más popular?'
    answer = model.ask_question(question)
    expected = 'Prueba'
    assert answer == expected
