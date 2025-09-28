import sys

# =================================================================
# 1. Framework Core Classes (com TestCase atualizado)
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

    # --- Novos métodos de asserção ---
    def assert_equal(self, first, second):
        if first != second:
            msg = f'"{first}" != "{second}"'
            raise AssertionError(msg)
    def assert_true(self, expr):
        if not expr:
            msg = f'"{expr}" is not true'
            raise AssertionError(msg)
    def assert_false(self, expr):
        if expr:
            msg = f'"{expr}" is not false'
            raise AssertionError(msg)
    def assert_in(self, member, container):
        if member not in container:
            msg = f'"{member}" not found in "{container}"'
            raise AssertionError(msg)

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
        return sorted([m for m in methods if m.startswith(self.TEST_METHOD_PREFIX)])
    def make_suite(self, test_case_class):
        suite = TestSuite()
        for name in self.get_test_case_names(test_case_class):
            suite.add_test(test_case_class(name))
        return suite

class TestRunner:
    def __init__(self):
        self.result = TestResult()
    def run(self, test):
        test.run(self.result)
        print(self.result.summary())
        return self.result

# =================================================================
# 2. Helper and All Test Classes (Refatoradas)
# =================================================================

class TestStub(TestCase):
    def test_success(self): self.assert_true(True)
    def test_failure(self): self.assert_false(True) # Usa assert_false para falhar
    def test_error(self): raise Exception("Error")

class TestSpy(TestCase):
    def __init__(self, name):
        super().__init__(name)
        self.log = ""
    def set_up(self): self.log += "set_up "
    def test_method(self): self.log += "test_method "
    def tear_down(self): self.log += "tear_down"

class TestCaseTest(TestCase):
    def set_up(self): self.result = TestResult()
    # Testes refatorados
    def test_result_success_run(self):
        TestStub('test_success').run(self.result)
        self.assert_equal('1 run, 0 failed, 0 error', self.result.summary())
    def test_result_failure_run(self):
        TestStub('test_failure').run(self.result)
        self.assert_equal('1 run, 1 failed, 0 error', self.result.summary())
    def test_result_error_run(self):
        TestStub('test_error').run(self.result)
        self.assert_equal('1 run, 0 failed, 1 error', self.result.summary())
    def test_result_multiple_run(self):
        suite = TestSuite()
        suite.add_test(TestStub('test_success'))
        suite.add_test(TestStub('test_failure'))
        suite.run(self.result)
        self.assert_equal('2 run, 1 failed, 0 error', self.result.summary())
    def test_template_method(self):
        spy = TestSpy('test_method')
        spy.run(self.result)
        self.assert_equal("set_up test_method tear_down", spy.log)
    def test_was_run(self):
        spy = TestSpy('test_method')
        spy.run(TestResult())
        self.assert_in("test_method", spy.log)
    def test_was_set_up(self):
        spy = TestSpy('test_method')
        spy.run(TestResult())
        self.assert_in("set_up", spy.log)
    def test_was_tear_down(self):
        spy = TestSpy('test_method')
        spy.run(TestResult())
        self.assert_in("tear_down", spy.log)

    # Novos testes para os asserts
    def test_assert_true(self):
        self.assert_true(True)
    def test_assert_false(self):
        self.assert_false(False)
    def test_assert_equal(self):
        self.assert_equal(1, 1)
        self.assert_equal("foo", "foo")
        self.assert_equal([], [])
        self.assert_equal({'a': 1}, {'a': 1})
    def test_assert_in(self):
        self.assert_in('a', 'abc')
        self.assert_in(1, [1, 2, 3])
        self.assert_in('key', {'key': 'value'})

class TestSuiteTest(TestCase):
    # Testes refatorados
    def test_suite_size(self):
        suite = TestSuite()
        suite.add_test(TestStub('test_success'))
        suite.add_test(TestStub('test_failure'))
        self.assert_equal(2, len(suite.tests))
    def test_suite_success_run(self):
        result, suite = TestResult(), TestSuite()
        suite.add_test(TestStub('test_success'))
        suite.run(result)
        self.assert_equal('1 run, 0 failed, 0 error', result.summary())
    def test_suite_multiple_run(self):
        result, suite = TestResult(), TestSuite()
        suite.add_test(TestStub('test_success'))
        suite.add_test(TestStub('test_failure'))
        suite.run(result)
        self.assert_equal('2 run, 1 failed, 0 error', result.summary())

class TestLoaderTest(TestCase):
    # Testes refatorados
    def test_create_suite(self):
        suite = TestLoader().make_suite(TestStub)
        self.assert_equal(3, len(suite.tests))
    def test_create_suite_of_suites(self):
        stub_suite = TestLoader().make_suite(TestStub)
        spy_suite = TestLoader().make_suite(TestSpy)
        suite = TestSuite()
        suite.add_test(stub_suite)
        suite.add_test(spy_suite)
        self.assert_equal(2, len(suite.tests))
    def test_get_multiple_test_case_names(self):
        names = TestLoader().get_test_case_names(TestStub)
        self.assert_equal(['test_error', 'test_failure', 'test_success'], names)
    def test_get_no_test_case_names(self):
        class EmptyTest(TestCase): pass
        names = TestLoader().get_test_case_names(EmptyTest)
        self.assert_equal([], names)

# =================================================================
# 3. Final Execution: Running All 19 Tests
# =================================================================

print("Executando TODOS os testes do framework (agora com 19 testes)...")

loader = TestLoader()
test_case_suite = loader.make_suite(TestCaseTest)
test_suite_suite = loader.make_suite(TestSuiteTest)
test_loader_suite = loader.make_suite(TestLoaderTest)

suite = TestSuite()
suite.add_test(test_case_suite)
suite.add_test(test_suite_suite)
suite.add_test(test_loader_suite)

runner = TestRunner()
runner.run(suite)