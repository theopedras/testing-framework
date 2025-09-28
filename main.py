import sys

# =================================================================
# 1. Framework Core Classes (versões finais)
# =================================================================

class TestResult:
    def __init__(self):
        self.run_count = 0
        self.failures = []
        self.errors = []

    def test_started(self):
        self.run_count += 1

    def add_failure(self, test_name, exception_info):
        self.failures.append((test_name, exception_info))

    def add_error(self, test_name, exception_info):
        self.errors.append((test_name, exception_info))

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
            result.add_failure(self.test_method_name, sys.exc_info())
        except Exception:
            result.add_error(self.test_method_name, sys.exc_info())
        finally:
            self.tear_down()

class TestSuite:
    def __init__(self):
        self.tests = []

    def add_test(self, test):
        self.tests.append(test)

    def run(self, result):
        for test in self.tests:
            test.run(result)

class TestLoader:
    TEST_METHOD_PREFIX = 'test'

    def get_test_case_names(self, test_case_class):
        methods = dir(test_case_class)
        test_method_names = sorted(list(filter(lambda method:
            method.startswith(self.TEST_METHOD_PREFIX), methods)))
        return test_method_names

    def make_suite(self, test_case_class):
        suite = TestSuite()
        for test_method_name in self.get_test_case_names(test_case_class):
            test_method = test_case_class(test_method_name)
            suite.add_test(test_method)
        return suite

class TestRunner:
    def __init__(self):
        self.result = TestResult()

    def run(self, test):
        test.run(self.result)
        print(self.result.summary())
        return self.result

# =================================================================
# 2. Helper Classes for Testing
# =================================================================

class TestStub(TestCase):
    def test_success(self):
        assert True
    def test_failure(self):
        assert False
    def test_error(self):
        raise Exception("Generic error")

class TestSpy(TestCase):
    def __init__(self, name):
        super().__init__(name)
    def test_method(self):
        pass

# =================================================================
# 3. Test Class for the New Components
# =================================================================

class TestLoaderTest(TestCase):
    def test_create_suite(self):
        loader = TestLoader()
        suite = loader.make_suite(TestStub)
        assert len(suite.tests) == 3

    def test_create_suite_of_suites(self):
        loader = TestLoader()
        stub_suite = loader.make_suite(TestStub)
        spy_suite = loader.make_suite(TestSpy)
        
        suite = TestSuite()
        suite.add_test(stub_suite)
        suite.add_test(spy_suite)
        
        assert len(suite.tests) == 2

    def test_get_multiple_test_case_names(self):
        loader = TestLoader()
        names = loader.get_test_case_names(TestStub)
        # O resultado de dir() pode variar, então ordenamos para um teste consistente
        assert names == ['test_error', 'test_failure', 'test_success']

    def test_get_no_test_case_names(self):
        class Test(TestCase):
            def foobar(self):
                pass
        
        loader = TestLoader()
        names = loader.get_test_case_names(Test)
        assert names == []

# =================================================================
# 4. Final, Simplified Execution Flow
# =================================================================

print("Executando TestLoaderTest com o novo fluxo (Loader + Runner)...")

# 1. O Loader descobre os testes automaticamente e cria a suíte.
loader = TestLoader()
suite = loader.make_suite(TestLoaderTest)

# 2. O Runner orquestra a execução e imprime o relatório.
runner = TestRunner()
runner.run(suite)