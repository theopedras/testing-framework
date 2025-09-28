# 1. Implementação da classe TestResult, conforme descrito na seção 3.
class TestResult:

    RUN_MSG = 'run'
    FAILURE_MSG = 'failed'
    ERROR_MSG = 'error'

    def __init__(self, suite_name=None):
        self.run_count = 0
        self.failures = []
        self.errors = []

    def test_started(self):
        self.run_count += 1

    def add_failure(self, test_name):
        self.failures.append(test_name)

    def add_error(self, test_name):
        self.errors.append(test_name)

    def summary(self):
        return f'{self.run_count} {self.RUN_MSG}, ' \
               f'{len(self.failures)} {self.FAILURE_MSG}, ' \
               f'{len(self.errors)} {self.ERROR_MSG}'

# 2. Classe TestCase atualizada com o método run() modificado.
class TestCase:

    def __init__(self, test_method_name):
        self.test_method_name = test_method_name

    def set_up(self):
        pass

    def tear_down(self):
        pass

    def run(self, result):
        result.test_started()
        self.set_up()
        try:
            test_method = getattr(self, self.test_method_name)
            test_method()
        except AssertionError as e:
            result.add_failure(self.test_method_name)
        except Exception as e:
            result.add_error(self.test_method_name)
        
        # Conforme o texto, tear_down() é chamado após o bloco try/except.
        # Uma implementação mais robusta usaria um bloco `finally` para garantir
        # que tear_down() execute mesmo se set_up() falhar.
        self.tear_down()

# 3. Classe de exemplo para demonstrar os diferentes resultados.
class ExampleTest(TestCase):
    
    def test_method_pass(self):
        # Este teste deve passar
        print("Executando test_method_pass...")
        pass

    def test_method_fail(self):
        # Este teste deve falhar (AssertionError)
        print("Executando test_method_fail...")
        assert 1 == 2

    def test_method_error(self):
        # Este teste deve gerar um erro (Exception)
        print("Executando test_method_error...")
        result = 1 / 0

# 4. Execução dos testes e exibição do sumário.
print("Iniciando a execução dos testes com coleta de resultados...")

# Cria a instância do coletor de resultados
result = TestResult()

# Executa o teste que passa
ExampleTest('test_method_pass').run(result)

# Executa o teste que falha
ExampleTest('test_method_fail').run(result)

# Executa o teste que gera erro
ExampleTest('test_method_error').run(result)

# Imprime o sumário final
print("\n--- Sumário ---")
print(result.summary())

# Opcional: ver quais testes falharam/erraram
print(f"Testes com falha: {result.failures}")
print(f"Testes com erro: {result.errors}")