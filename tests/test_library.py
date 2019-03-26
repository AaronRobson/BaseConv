#!/usr/bin/python

import unittest
from hypothesis import given
import hypothesis.strategies as st
import string

from baseconv import IntoDec, FromDec, BasCalc, MINIMUM_BASE


class TestBaseConvClass(unittest.TestCase):

    def testIntoDec(self):
        self.assertEqual(IntoDec(10, 2), 2, 'from binary')
        self.assertEqual(IntoDec(-10, 2), -2, 'from binary negative')
        self.assertEqual(IntoDec(101010, 2), 42, 'from binary 42')
        self.assertEqual(IntoDec('9', 10), 9, 'under boundary condition')

    def testFromDec(self):
        self.assertEqual(FromDec(15, 16), 'F', 'edge')
        self.assertEqual(FromDec(-15, 16), '-F', 'edge minus')
        self.assertEqual(FromDec(42, 2), '101010', 'to binary')

    @given(
        number=st.integers(),
        base=st.integers(
            min_value=MINIMUM_BASE,
            max_value=len(string.ascii_uppercase)))
    def test_convert_FromDec_is_reverted_by_IntoDec(self, number, base):
        self.assertEqual(IntoDec(FromDec(number, base), base), number)

    def testBasCalc(self):
        self.assertEqual(BasCalc(101010, 2, 10), '42', 'binary to decimal')
        self.assertEqual(BasCalc('101010', '2', '10'), '42',
                         'text binary to decimal')
        self.assertEqual(BasCalc(42, 10, 2), '101010', 'decimal to binary')
        self.assertEqual(BasCalc('101010', inBas=2), '42',
                         'default out base, named in base')
        self.assertEqual(BasCalc(42, outBas=2), '101010',
                         'default in base, named out base')
        self.assertEqual(BasCalc(15, inBas=6, outBas=4), '23',
                         'named in and out bases')
        self.assertEqual(BasCalc('FF', 16, 2), '11111111', 'hex to binary')
        self.assertEqual(BasCalc(11111111, 2, 16), 'FF', 'binary to hex')
        self.assertEqual(BasCalc('400', 16, 10), '1024', 'hex to decimal')

        self.assertEqual(BasCalc('-567', 10, 10), '-567',
                         'minus number decimal to decimal')

        for i in range(1000):
            self.assertEqual(BasCalc('DEADBEEF', 16, 2),
                             '11011110101011011011111011101111')


if __name__ == "__main__":
    unittest.main()
