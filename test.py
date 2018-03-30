#!/usr/bin/python

import unittest

import BaseConv
import BaseConvGUI

class TestBaseConvClass(unittest.TestCase):
    def setUp(self):
        self.support = BaseConv

    """
    def testCharToVal(self):
        self.assertEqual(self.support._CharToVal('1'), 1, 'CharToVal Fail: standard lower inclusive boundary.')
        self.assertEqual(self.support._CharToVal('9'), 9, 'CharToVal Fail: standard upper inclusive boundary.')
        self.assertEqual(self.support._CharToVal('A'), 10, 'CharToVal Fail: non-standard lower inclusive boundary.')
        self.assertEqual(self.support._CharToVal('Z'), 35, 'CharToVal Fail: non-standard upper inclusive boundary.')

    def testValToChar(self):
        self.assertEqual(self.support._ValToChar('0'), '0', 'ValToChar Fail: standard lower inclusive boundary from string.')
        self.assertEqual(self.support._ValToChar(0), '0', 'ValToChar Fail: standard lower inclusive boundary.')
        self.assertEqual(self.support._ValToChar(9), '9', 'ValToChar Fail: standard upper inclusive boundary.')
        self.assertEqual(self.support._ValToChar(10), 'A', 'ValToChar Fail: non-standard lower inclusive boundary.')
        self.assertEqual(self.support._ValToChar(35), 'Z', 'ValToChar Fail: non-standard upper inclusive boundary.')
        self.assertRaises(self.support.InvalidInternalValueError, lambda _: self.support._ValToChar(-1), 'ValToChar Fail: beyond lower band.')
        self.assertRaises(self.support.InvalidInternalValueError, lambda _: self.support._ValToChar(36), 'ValToChar Fail: beyond upper band.')

    def testValidNum(self):
        self.assertEqual(self.support._ValidNum(0), '0', 'ValidNum Fail: standard lower inclusive boundary.')
        self.assertEqual(self.support._ValidNum(9), '9', 'ValidNum Fail: standard upper inclusive boundary.')
        self.assertEqual(self.support._ValidNum('a'), 'A', 'ValidNum Fail: non-standard lower inclusive boundary.')
        self.assertEqual(self.support._ValidNum('z'), 'Z', 'ValidNum Fail: non-standard upper inclusive boundary.')

        self.assertEqual(self.support._ValidNum('-0'), '0', 'ValidNum Fail: minus zero allowed.')
        self.assertEqual(self.support._ValidNum('00'), '0', 'ValidNum Fail: leading zeros not stripped.')
        self.assertEqual(self.support._ValidNum('-00'), '0', 'ValidNum Fail: leading zeros not stripped when minused.')
        self.assertEqual(self.support._ValidNum('01'), '1', 'ValidNum Fail: leading zero not removed for positive number.')
        self.assertEqual(self.support._ValidNum('-01'), '-1', 'ValidNum Fail: leading zero not removed for negative number.')

        #Error messages must be as literals on the same line as the error so they are printed to the screen with the offending line.
        #'ValidNum Fail: random nonsense is accepted.', self.assertRaises(self.support.InvalidNumberError, self.support._ValidNum, '#=[];.')
        self.assertRaises(self.support.InvalidNumberError, lambda _: self.support._ValidNum('#=[];.'), 'ValidNum Fail: random nonsense is accepted.')

    def testValidBas(self):
        self.assertEqual(self.support._ValidBas(2), 2, 'ValidBas fail: above lower boundary')
        self.assertEqual(self.support._ValidBas(10), 10, 'ValidBas fail: standard decimal')
        self.assertEqual(self.support._ValidBas('10'), 10, 'ValidBas fail: standard decimal from string')
    """
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
    """
    def testValidInputNumForBas(self):
        'ValidInputNumForBas fail: number given as string', self.support._ValidInputNumForBas(9, 10)
        'ValidInputNumForBas fail: within boundary condition', self.support._ValidInputNumForBas('9', 10)
        'ValidInputNumForBas fail: within boundary condition default base', self.support._ValidInputNumForBas('9')
        'ValidInputNumForBas fail: beyond boundary condition default base', self.assertRaises(self.support.InvalidInputBaseError, self.support._ValidInputNumForBas, 'A')
        'ValidInputNumForBas fail: beyond boundary condition', self.assertRaises(self.support.InvalidInputBaseError, self.support._ValidInputNumForBas, 'A', 10)
        'ValidInputNumForBas fail minus value:', self.support._ValidInputNumForBas('-34', 10)
    """

if __name__ == "__main__":
    unittest.main()
