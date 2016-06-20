#!/usr/bin/python

from string import digits, ascii_uppercase #, ascii_lowercase
from Decorators.decorators import memoised

MINUS_SIGN = '-'
ZERO = '0'

DEFAULT_BASE = 10
MINIMUM_BASE = 2

#the index of a character in this collection should give the value (as long as the character is uppercased in standard notation)
ALLOWED_SYMBOLS = digits + ascii_uppercase # + ascii_lowercase

#http://en.wikipedia.org/wiki/Radix
class BaseConvError(Exception): #generic attributes for all custom exceptions
	def __str__(self):
		return str(self._value) # __repr__ defaults to the value of __str__ when missing

class InvalidNumberError(BaseConvError):
	_value = 'Invalid Number'

class InvalidBaseError(BaseConvError):
	_value = 'Invalid Base'

class InvalidInputBaseError(InvalidBaseError):
	_value = 'Invalid Input Base'

class InvalidInternalValueError(BaseConvError):
	_value = 'Invalid Internal Value Error'

def _ValidNum(value):
	'''Returns a string representing the number given validated to standard notation:
	no leading zeros (with or without a minus sign) and all letters in uppercase format.

	Throws InvalidNumberError on data with disallowed symbols.'''

	# does not presume to assume if the number is int that it must be decimal as it could also represent any other lower base
	value = str(value).strip()
	# would if not alpha try converting to int and letting conversion errors not be caught and go straight to the call (or be replaced by a custom InvalidBaseError exception), however this way just removes all non-allowed characters instead
	value = value.upper()

	minused = value.startswith(MINUS_SIGN)
	#remove minus sign if present
	if minused:
		value = value[1:]

	#remove any leading zeros
	value = value.lstrip(ZERO)

	if value:
		for char in value:
			if not char in ALLOWED_SYMBOLS:
				raise InvalidNumberError
		else:
			return (MINUS_SIGN * minused) + value		
	else:
		return ZERO

def _ValidBas(value):
	'''Returns an int with a value of 2 or above or
	raises InvalidBaseError exception.
	'''
	value = str(value).strip()

	if not value:
		value = DEFAULT_BASE

	try:
		# nominal case
		intValue = int(value)
	except ValueError:
		raise InvalidBaseError
	else:
		if MINIMUM_BASE <= intValue:
			return intValue # nominal case
		else:
			raise InvalidBaseError
"""
def _ValidInputNumForBas(num, bas=DEFAULT_BASE):
	try:
		bas = int(bas)
	except ValueError:
		raise InvalidInputBaseError
	else:
		num = str(num)

		if num[0] == MINUS_SIGN:
			num = num[1:]

		for i in str(num):
			if bas <= CharToVal(i):
				raise InvalidInputBaseError
"""
"""
def _CharToVal(inputChar):
	try:
		return ALLOWED_SYMBOLS.index(inputChar)
	except ValueError:
		raise InvalidInternalValueError
"""

def _ValToChar(inputNum):
	try:
		inputNum = int(inputNum)
	except ValueError:
		raise InvalidInternalValueError

	# Negative indexes count backwards from the end of the list
	if inputNum < 0:
		raise InvalidInternalValueError

	try:
		return ALLOWED_SYMBOLS[inputNum]
	except IndexError:
		raise InvalidInternalValueError

@memoised
def IntoDec(inNum, inBas):
	'''Returns an int.
	'''
	inNum = _ValidNum(inNum)
	inBas = _ValidBas(inBas)
	try:
		return int(inNum, inBas)
	except ValueError:
		raise InvalidInputBaseError

@memoised
def FromDec(inNum, outBas):
	'''Is an error for inNum to not be an integer.
	'''
	try:
		inNum = int(_ValidNum(inNum))
	except ValueError:
		raise InvalidNumberError

	outBas = _ValidBas(outBas)

	minused = inNum < 0
	if minused:
		inNum *= -1

	values = []
	while (0 < inNum):
		#is quicker to put in a list and then join at the end
		values.append(_ValToChar(inNum % outBas))
		inNum //= outBas

	value = ''.join(reversed(values))
 
	if value:
		return (MINUS_SIGN * minused) + value 
	else:
		return ZERO

def BasCalc(inNum, inBas=DEFAULT_BASE, outBas=DEFAULT_BASE):
	'''Given a number and its current base, returns the number with a new specified base.
	If a base is not given it is assumed to be base %d.
	''' % (DEFAULT_BASE)
	return FromDec(IntoDec(inNum, inBas), outBas)

def _CommandLine(args):
	if 1 < len(args):
		for arg in args[1:]:
			if arg in ('-h', '--help'):
				print('This program converts integers which may be signed between any two number bases %d and over.\nInputs as follows:\ninNum = the Input Number\ninBas = the Input Base\noutBas = the Output Base' % (MINIMUM_BASE))
				break
			elif arg in ('-t', '--test'):
				import test
				test.RunTests()
				break
		else:
			print(BasCalc(*args[1:]))
	else:
		print('Base Converter')
		exitVals = ('q', 'quit')
		while True:
			try:
				print('Output Number: ' + BasCalc(input('\nEnter an Input Number: ').strip(), input('Enter an Input Base: ').strip(), input('Enter an Output Base: ').strip()))
			except (BaseConvError, ValueError) as e:
				print('Error: ', e)
			if input('\nEnter any of the following values to exit: %s\nor press return to continue: ' % (str(exitVals))).strip().lower() in exitVals:
				break

if __name__ == "__main__":
	from sys import argv
	_CommandLine(argv)

	#keep the window open
	#input('\nPress Enter to Exit:')
