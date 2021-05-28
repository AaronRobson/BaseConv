#!/usr/bin/python

import unittest
from hypothesis import given
import hypothesis.strategies as st
import string

from baseconv import into_dec, from_dec, bas_calc, MINIMUM_BASE


class TestBaseConvClass(unittest.TestCase):

    def test_into_dec(self):
        self.assertEqual(into_dec(10, 2), 2, 'from binary')
        self.assertEqual(into_dec(-10, 2), -2, 'from binary negative')
        self.assertEqual(into_dec(101010, 2), 42, 'from binary 42')
        self.assertEqual(into_dec('9', 10), 9, 'under boundary condition')

    def test_from_dec(self):
        self.assertEqual(from_dec(15, 16), 'F', 'edge')
        self.assertEqual(from_dec(-15, 16), '-F', 'edge minus')
        self.assertEqual(from_dec(42, 2), '101010', 'to binary')

    @given(
        number=st.integers(),
        base=st.integers(
            min_value=MINIMUM_BASE,
            max_value=len(string.ascii_uppercase)))
    def test_convert_from_dec_is_reverted_by_into_dec(self, number, base):
        self.assertEqual(into_dec(from_dec(number, base), base), number)

    def test_bas_calc(self):
        self.assertEqual(bas_calc(101010, 2, 10), '42', 'binary to decimal')
        self.assertEqual(bas_calc('101010', '2', '10'), '42',
                         'text binary to decimal')
        self.assertEqual(bas_calc(42, 10, 2), '101010', 'decimal to binary')
        self.assertEqual(bas_calc('101010', in_bas=2), '42',
                         'default out base, named in base')
        self.assertEqual(bas_calc(42, out_bas=2), '101010',
                         'default in base, named out base')
        self.assertEqual(bas_calc(15, in_bas=6, out_bas=4), '23',
                         'named in and out bases')
        self.assertEqual(bas_calc('FF', 16, 2), '11111111', 'hex to binary')
        self.assertEqual(bas_calc(11111111, 2, 16), 'FF', 'binary to hex')
        self.assertEqual(bas_calc('400', 16, 10), '1024', 'hex to decimal')

        self.assertEqual(bas_calc('-567', 10, 10), '-567',
                         'minus number decimal to decimal')

        for i in range(1000):
            self.assertEqual(bas_calc('DEADBEEF', 16, 2),
                             '11011110101011011011111011101111')


if __name__ == "__main__":
    unittest.main()
