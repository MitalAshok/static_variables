import os.path
import sys
import unittest

__dir__ = os.path.abspath(os.path.dirname(__file__))

sys.path.insert(0, os.path.dirname(__dir__))

try:
    import static_variables
finally:
    sys.path.pop(0)

static = static_variables.static
t = static_variables.resolve_static
NO_VALUE = static_variables.NO_VALUE
EMPTY_SET = static_variables.EMPTY_SET


class TestStaticVariables(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if sys.version_info < (3, 6):
            raise Exception('Cannot run tests on this python version (' + sys.version + ')')
        import platform

        imp = platform.python_implementation()
        if imp != 'CPython':
            raise Exception('Cannot run tests on this python implementation (' + imp + ')')
        if static_variables.check_static() != 0:
            raise Exception('static_variables.check_static() failed')

    def test_static_constants(self):
        @t
        def f():
            one = static(1)
            two = int(static('2'))
            return one + two

        self.assertEqual(f(), 3)

    def test_static_binary_ops(self):
        ONE = 1
        TWO = 2
        @t
        def f():
            three = static(ONE + 2)
            four = static(2 * TWO)
            return three + four

        self.assertEqual(f(), 7)

    def test_nested_function(self):
        @t
        def f():
            three = static(1 + int('2'))
            one = static(1 .__int__())
            _one = ~static(int(('<>' in '~') != (hasattr(str, ''))))
            return three + one + _one

        self.assertEqual(f(), 3)

    def test_methods(self):
        class Test(object):
            @t
            def test(self):
                return static([])

        test = Test().test
        ls = test()
        self.assertEqual(ls, [])
        self.assertIs(ls, test())
        ls.append(3)
        self.assertEqual(test(), [3])

    def test_containers(self):
        @t
        def f():
            ls = static([self, 1, 2, ()])
            ls_e = static([])
            tpl = static((self, '23', 23, [1, 23, 5]))
            tpl_e = static(())
            dct = static({
                'self': self,
                't': [1]
            })
            dct_e = static({})
            st = static({1, 2, 3, 4, (1, 2, 3, 4)})
            st_e = static(set())
            return (
                ls, ls_e, tpl, tpl_e, dct, dct_e, st, st_e
            )

        ret = f()
        ls, ls_e, tpl, tpl_e, dct, dct_e, st, st_e = ret
        for a, b in zip(ret, f()):
            self.assertIs(a, b)
        self.assertIs(ls[0], self)

    def test_mutations(self):
        @t
        def f():
            return static([])

        ls = f()
        f().append(2)
        self.assertEqual(ls, [2])
        self.assertIs(ls, f())

    def test_redundant_constants(self):
        @t
        def f():
            return static(None), static(None), static(None), static(None), static(None), static(None)

        self.assertLess(len(static_variables.codetools.get_attr(f, 'co_consts')), 3)

    def test_empty_set_literal(self):
        @t(empty_set_literal=True)
        def f():
            return {}

        @t
        def g():
            return EMPTY_SET

        for func in (f, g):
            empty_set = func()
            self.assertFalse(empty_set)
            self.assertEqual(empty_set, set())
            self.assertNotEqual(empty_set, {})
            self.assertIsNot(empty_set, func())

    def test_generators(self):
        @t
        def f():
            while True:
                yield static([])

        g = f()

        if hasattr(type(g), 'next'):
            next_ = type(g).next
        else:
            next_ = next

        ls = next_(g)
        next_(g).append(2)
        self.assertEqual(ls, [2])
        self.assertIs(ls, next_(g))

    def test_static_variables(self):
        @t(static_variables={'t': NO_VALUE})
        def f():
            try:
                t += 1
            except NameError:
                t = 0
            return t

        self.assertEqual(f(), 0)
        self.assertEqual(f(), 1)
        self.assertEqual(f(), 2)

        def get_free_name_error():
            def closure():
                return t
            if False:
                t = True
            try:
                closure()
            except NameError as e:
                return e
            self.assertFalse(True, 'Did not raise NameError')

        @t(static_variables={'t': NO_VALUE})
        def f():
            return t

        try:
            f()
            with self.assertRaises(NameError):
                pass
        except NameError as e:
            self.assertEqual(repr(e), repr(get_free_name_error()))

        @t(static_variables={'t': 1})
        def f():
            return t

        self.assertEqual(f(), 1)

    def test_static_empty_set(self):
        @t(empty_set_literal=True)
        def f():
            return static({}), static(EMPTY_SET)

        a, b = f()
        c, d = f()
        self.assertIs(a, c)
        self.assertIs(b, d)

    def test_invalid(self):
        with self.assertRaises(SyntaxError):
            @t
            def f():
                return static(static([]))

        with self.assertRaises(SyntaxError):
            @t
            def f():
                return static


if __name__ == '__main__':
    unittest.main()
