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


class TestStaticVariables(unittest.TestCase):
    def test_static_constants(self):
        @t
        def f():
            one = static(1)
            two = int(static('2'))
            return one + two

        # print('Dissassembling...')
        # print('Undecorated:')
        # __import__('dis').dis(f)
        # c = f.__code__.co_code
        # f = t(f)
        # print('Decorated:')
        # __import__('dis').dis(f)
        # print(c)
        # print(f.__code__.co_code)

        self.assertEqual(f(), 3)

    def test_static_binary_ops(self):
        @t
        def f():
            three = static(1 + 2)
            four = static(2 * 2)
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
        if sys.version_info < (3, 6):
            return # Untested on 3.5, doesn't seem to work on 3.4
        @t
        def f():
            return static([])

        ls = f()
        f().append(2)
        self.assertEqual(ls, [2])
        self.assertIs(ls, f())

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


if __name__ == '__main__':
    unittest.main()
