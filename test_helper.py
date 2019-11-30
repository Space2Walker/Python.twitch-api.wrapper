import unittest

import helper


def dummy(**kwargs):
    return kwargs


class TestKwargsToString(unittest.TestCase):
    def test_kwargs_function(self):
        # test int
        self.assertEqual(helper.kwargs_to_query(dummy(id=100)), 'id=100')
        self.assertEqual(helper.kwargs_to_query(dummy(id=[100, 200])), 'id=100&id=200')
        # test str
        self.assertEqual(helper.kwargs_to_query(dummy(st='foo')), 'st=foo')
        self.assertEqual(helper.kwargs_to_query(dummy(st=['foo', 'bar'])), 'st=foo&st=bar')
        # test combine
        self.assertEqual(helper.kwargs_to_query(dummy(id=['100', 200],
                                                      name=['foo', 'bar'],
                                                      y=123,
                                                      x='sdf')),
                         'id=100&id=200&name=foo&name=bar&y=123&x=sdf')

    def test_kwargs_value(self):
        # test negative int
        with self.assertRaises(ValueError):
            helper.kwargs_to_query(dummy(foo=-1))
        with self.assertRaises(ValueError):
            helper.kwargs_to_query(dummy(foo=[-1, -2]))

    def test_kwargs_type(self):
        # test float
        with self.assertRaises(TypeError):
            helper.kwargs_to_query(dummy(foo=1.5))
        with self.assertRaises(TypeError):
            helper.kwargs_to_query(dummy(foo=[1.5, 2.3]))

        # test dict
        with self.assertRaises(TypeError):
            helper.kwargs_to_query(dummy(foo={'k': 'v'}))
        with self.assertRaises(TypeError):
            helper.kwargs_to_query(dummy(foo=[{'k': 'v'}, {'k': 'v'}]))

        # test complex
        with self.assertRaises(TypeError):
            helper.kwargs_to_query(dummy(foo=5j))
        with self.assertRaises(TypeError):
            helper.kwargs_to_query(dummy(foo=[1j, 2j]))

        # test bool
        with self.assertRaises(TypeError):
            helper.kwargs_to_query(dummy(foo=True))
        with self.assertRaises(TypeError):
            helper.kwargs_to_query(dummy(foo=[True, False]))


if __name__ == '__main__':
    unittest.main()
