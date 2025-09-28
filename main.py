# =================================================================
# 1. Framework Core Classes (das seções anteriores)
# =================================================================

class TestResult:
    def __init__(self):
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
        return (f'{self.run_count} run, '
                f'{len(self.failures)} failed, '
                f'{len(self.errors)} error')

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
            method = getattr(self, self.test_method_name)
            method()
        except AssertionError:
            result.add_failure(self.test_method_name)
        except Exception:
            result.add_error(self.test_method_name)
        finally:
            self.tear_down()

# =================================================================
# 2. Nova Classe TestSuite (implementação da Seção 5)
# =================================================================

class TestSuite:
    def __init__(self):
        self.tests = []

    def add_test(self, test):
        self.tests.append(test)

    def run(self, result):
        for test in self.tests:
            test.run(result)

# =================================================================
# 3. Classes de Teste e Auxiliares
# =================================================================

# Classe auxiliar (stub) para testes
class TestStub(TestCase):
    def test_success(self):
        assert True

    def test_failure(self):
        assert False

    def test_error(self):
        raise Exception("Generic error")

# Classe de teste para TestCase
class TestCaseTest(TestCase):
    def set_up(self):
        self.result = TestResult()
        
    def test_result_success_run(self):
        stub = TestStub('test_success')
        stub.run(self.result)
        assert self.result.summary() == '1 run, 0 failed, 0 error'

    def test_result_failure_run(self):
        stub = TestStub('test_failure')
        stub.run(self.result)
        assert self.result.summary() == '1 run, 1 failed, 0 error'

    def test_result_error_run(self):
        stub = TestStub('test_error')
        stub.run(self.result)
        assert self.result.summary() == '1 run, 0 failed, 1 error'

    def test_result_multiple_run(self):
        suite = TestSuite()
        suite.add_test(TestStub('test_success'))
        suite.add_test(TestStub('test_failure'))
        suite.run(self.result)
        assert self.result.summary() == '2 run, 1 failed, 0 error'
        
    def test_template_method(self):
        class TestSpy(TestCase):
            def __init__(self, name):
                super().__init__(name)
                self.log = ""
            def set_up(self):
                self.log += "set_up "
            def test_method(self):
                self.log += "test_method "
            def tear_down(self):
                self.log += "tear_down"
        
        spy = TestSpy('test_method')
        spy.run(self.result)
        assert spy.log == "set_up test_method tear_down"

# Nova classe de teste para TestSuite
class TestSuiteTest(TestCase):

    def test_suite_size(self):
        suite = TestSuite()
        suite.add_test(TestStub('test_success'))
        suite.add_test(TestStub('test_failure'))
        suite.add_test(TestStub('test_error'))
        assert len(suite.tests) == 3

    def test_suite_success_run(self):
        result = TestResult()
        suite = TestSuite()
        suite.add_test(TestStub('test_success'))
        suite.run(result)
        assert result.summary() == '1 run, 0 failed, 0 error'

    def test_suite_multiple_run(self):
        result = TestResult()
        suite = TestSuite()
        suite.add_test(TestStub('test_success'))
        suite.add_test(TestStub('test_failure'))
        suite.add_test(TestStub('test_error'))
        suite.run(result)
        assert result.summary() == '3 run, 1 failed, 1 error'

# =================================================================
# 4. Execução de todos os testes via TestSuite
# =================================================================

print("Executando todos os testes do framework via TestSuite...")

# Cria o coletor de resultados e a suíte principal
result = TestResult()
suite = TestSuite()

# Adiciona todos os 5 testes de TestCaseTest à suíte
suite.add_test(TestCaseTest('test_result_success_run'))
suite.add_test(TestCaseTest('test_result_failure_run'))
suite.add_test(TestCaseTest('test_result_error_run'))
suite.add_test(TestCaseTest('test_result_multiple_run'))
suite.add_test(TestCaseTest('test_template_method'))

# Adiciona todos os 3 testes de TestSuiteTest à suíte
suite.add_test(TestSuiteTest('test_suite_size'))
suite.add_test(TestSuiteTest('test_suite_success_run'))
suite.add_test(TestSuiteTest('test_suite_multiple_run'))

# Executa a suíte de testes inteira
suite.run(result)

# Imprime o sumário final
print("\n--- Sumário Final ---")
print(result.summary())