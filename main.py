# 1. A implementação inicial da classe TestCase
class TestCase:

    def __init__(self, test_method_name):
        self.test_method_name = test_method_name

    def run(self):
        self.set_up()    # chama método de setup
        test_method = getattr(self, self.test_method_name)
        test_method()    # chama método de teste 
        self.tear_down() # chama método de teardown 

    def set_up(self):
        # Este método pode ser sobrescrito pelas subclasses
        pass

    def tear_down(self):
        # Este método pode ser sobrescrito pelas subclasses
        pass

# 2. A classe de teste de exemplo que estende de TestCase
class MyTest(TestCase):

    def set_up(self):
        print('set_up')

    def tear_down(self):
        print('tear_down')

    def test_a(self):
        print('test_a')

    def test_b(self):
        print('test_b')

    def test_c(self):
        print('test_c')

# 3. Execução dos métodos de teste
print("Iniciando a execução dos testes...")

test = MyTest('test_a')
test.run()

test = MyTest('test_b')
test.run()

test = MyTest('test_c')
test.run()

print("Execução dos testes finalizada.")
