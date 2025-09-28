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
            # Usar `finally` é mais robusto para garantir que tear_down sempre rode
            self.tear_down()

# =================================================================
# 2. Helper Classes for Testing (descritas na Seção 4)
# =================================================================

# TestStub simula testes com diferentes resultados
class TestStub(TestCase):
    def test_success(self):
        assert True

    def test_failure(self):
        assert False

    def test_error(self):
        raise Exception("This is a generic error")

# TestSpy "espiona" a execução do template method
class TestSpy(TestCase):
    def __init__(self, name):
        super().__init__(name)
        self.was_run = False
        self.was_set_up = False
        self.was_tear_down = False
        self.log = ""

    def set_up(self):
        self.was_set_up = True
        self.log += "set_up "

    def test_method(self):
        self.was_run = True
        self.log += "test_method "

    def tear_down(self):
        self.was_tear_down = True
        self.log += "tear_down"

# =================================================================
# 3. The Test Class for TestCase (a classe principal desta seção)
# =================================================================

class TestCaseTest(TestCase):
    def set_up(self):
        self.result = TestResult()

    # Testes usando TestStub
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
        TestStub('test_success').run(self.result)
        TestStub('test_failure').run(self.result)
        TestStub('test_error').run(self.result)
        assert self.result.summary() == '3 run, 1 failed, 1 error'

    # Testes usando TestSpy
    def test_was_set_up(self):
        spy = TestSpy('test_method')
        spy.run(self.result)
        assert spy.was_set_up

    def test_was_run(self):
        spy = TestSpy('test_method')
        spy.run(self.result)
        assert spy.was_run

    def test_was_tear_down(self):
        spy = TestSpy('test_method')
        spy.run(self.result)
        assert spy.was_tear_down

    def test_template_method(self):
        spy = TestSpy('test_method')
        spy.run(self.result)
        assert spy.log == "set_up test_method tear_down"

# =================================================================
# 4. Execution of the Tests
# =================================================================
print("Executando os testes da classe TestCaseTest...")

result = TestResult()

# Executa todos os 8 métodos de teste de TestCaseTest
TestCaseTest('test_result_success_run').run(result)
TestCaseTest('test_result_failure_run').run(result)
TestCaseTest('test_result_error_run').run(result)
TestCaseTest('test_result_multiple_run').run(result)
TestCaseTest('test_was_set_up').run(result)
TestCaseTest('test_was_run').run(result)
TestCaseTest('test_was_tear_down').run(result)
TestCaseTest('test_template_method').run(result)

print("\n--- Sumário Final ---")
print(result.summary())