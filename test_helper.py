import unittest

import helper


def dummy(**kwargs):
    return kwargs


class TestHelper(unittest.TestCase):
    def test_kwargs_to_string(self):
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
        # test float raise
        with self.assertRaises(Exception):
            helper.kwargs_to_query(dummy(foo=1.5))
        with self.assertRaises(Exception):
            helper.kwargs_to_query(dummy(foo=[1.5, 2.3]))
        # test dict raise
        with self.assertRaises(Exception):
            helper.kwargs_to_query(dummy(foo={'k': 'v'}))
        with self.assertRaises(Exception):
            helper.kwargs_to_query(dummy(foo=[{'k': 'v'}, {'k': 'v'}]))


if __name__ == '__main__':
    unittest.main()
