#!/usr/bin/python

import unittest

import baseconv

class TestBaseConvClass(unittest.TestCase):
    def setUp(self):
        self.support = baseconv

    def testIntoDec(self):
        self.assertEqual(self.support.IntoDec(10, 2), 2, 'IntoDec Fail: from binary simple.')
        self.assertEqual(self.support.IntoDec(-10, 2), -2, 'IntoDec Fail: from binary simple but negative.')
        self.assertEqual(self.support.IntoDec(101010, 2), 42, 'IntoDec Fail: from binary complex 42.')
        self.assertEqual(self.support.IntoDec('9', 10), 9, 'IntoDec fail: under boundary condition')

    def testFromDec(self):
        self.assertEqual(self.support.FromDec(15, 16), 'F', 'FromDec Fail: edge.')
        self.assertEqual(self.support.FromDec(-15, 16), '-F', 'FromDec Fail: edge minus.')
        self.assertEqual(self.support.FromDec(42, 2), '101010', 'FromDec Fail: to boolean')
      
    def testBasCalc(self):
        self.assertEqual(self.support.BasCalc(101010, 2, 10), '42', 'BasCalc Fail: binary to decimal.')
        self.assertEqual(self.support.BasCalc('101010', '2', '10'), '42', 'BasCalc Fail: text binary to decimal.')
        self.assertEqual(self.support.BasCalc(42, 10, 2), '101010', 'BasCalc Fail: decimal to binary.')
        self.assertEqual(self.support.BasCalc('101010', inBas=2), '42', 'BasCalc fail: default out base with named in base.')
        self.assertEqual(self.support.BasCalc(42, outBas=2), '101010', 'BasCalc Fail: default in base with named out base.')
        self.assertEqual(self.support.BasCalc(15, inBas=6, outBas=4), '23', 'BasCalc fail: non standard named in and out bases')
        self.assertEqual(self.support.BasCalc('FF', 16, 2), '11111111', 'BasCalc Fail: large hex to binary.')
        self.assertEqual(self.support.BasCalc(11111111, 2, 16), 'FF', 'BasCalc Fail: large binary to hex.')
        self.assertEqual(self.support.BasCalc('400', 16, 10), '1024', 'BasCalc Fail: large hex to decimal.')

        self.assertEqual(self.support.BasCalc('-567', 10, 10), '-567', 'BasCalc Fail: minus number incorrectly handled in simple decimal to decimal case.')

        for i in range(1000):
          self.assertEqual(self.support.BasCalc('DEADBEEF', 16, 2), '11011110101011011011111011101111', '')

if __name__ == "__main__":
    unittest.main()
