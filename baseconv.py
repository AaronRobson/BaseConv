#!/usr/bin/python

from string import digits, ascii_uppercase

from six.moves import input

MINUS_SIGN = '-'
ZERO = '0'

DEFAULT_BASE = 10
MINIMUM_BASE = 2

# the index of a character in this collection should give the value
# (as long as the character is uppercased in standard notation)
ALLOWED_SYMBOLS = digits + ascii_uppercase

# http://en.wikipedia.org/wiki/Radix


class BaseConvError(Exception):
    '''Generic attributes for all custom exceptions.
    '''

    def __str__(self):
        '''__repr__ defaults to the value of __str__ when missing.
        '''
        return str(self._value)


class InvalidNumberError(BaseConvError):
    _value = 'Invalid Number'


class InvalidBaseError(BaseConvError):
    _value = 'Invalid Base'


class InvalidInputBaseError(InvalidBaseError):
    _value = 'Invalid Input Base'


class InvalidInternalValueError(BaseConvError):
    _value = 'Invalid Internal Value Error'


def _ValidNum(value):
    '''Return a string representing the number given validated to
    standard notation:
    no leading zeros (with optional minus sign)
    all letters in uppercase format.

    Throws InvalidNumberError on data with disallowed symbols.
    '''

    # does not presume to assume if the number is int that it must be decimal
    # as it could also represent any other lower base
    value = str(value).strip()
    # would if not alpha try converting to int and letting conversion errors
    # not be caught and go straight to the call (or be replaced by a custom
    # InvalidBaseError exception), however this way just removes all
    # non-allowed characters instead
    value = value.upper()

    minused = value.startswith(MINUS_SIGN)
    # remove minus sign if present
    if minused:
        value = value[1:]

    # remove any leading zeros
    value = value.lstrip(ZERO)

    if value:
        for char in value:
            if char not in ALLOWED_SYMBOLS:
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
            # nominal case
            return intValue
        else:
            raise InvalidBaseError


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


def IntoDec(inNum, inBas):
    '''Returns an int.
    '''
    inNum = _ValidNum(inNum)
    inBas = _ValidBas(inBas)
    try:
        return int(inNum, inBas)
    except ValueError:
        raise InvalidInputBaseError


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
        values.append(_ValToChar(inNum % outBas))
        inNum //= outBas

    value = ''.join(reversed(values))

    if value:
        return (MINUS_SIGN * minused) + value
    else:
        return ZERO


def BasCalc(inNum, inBas=DEFAULT_BASE, outBas=DEFAULT_BASE):
    '''Given a number and its current base, returns the number with a
    new specified base.
    If a base is not given it is assumed to be base %d.
    ''' % (DEFAULT_BASE)
    return FromDec(IntoDec(inNum, inBas), outBas)


def _CommandLine(args):
    if 1 < len(args):
        for arg in args[1:]:
            if arg in ('-h', '--help'):
                print('This program converts integers which may be signed ' +
                      'between any two number bases %d and over.\n' +
                      'Inputs as follows:\n' +
                      'inNum = the Input Number\n' +
                      'inBas = the Input Base\n' +
                      'outBas = the Output Base' % (MINIMUM_BASE))
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
                print('Output Number: ' +
                      BasCalc(input('\nEnter an Input Number: ').strip(),
                              input('Enter an Input Base: ').strip(),
                              input('Enter an Output Base: ').strip()))
            except (BaseConvError, ValueError) as e:
                print('Error: ', e)
            if input('\nEnter any of the following values to exit: %s\n' +
                     'or press return to continue: ' %
                     (str(exitVals))).strip().lower() in exitVals:
                break


if __name__ == "__main__":
    from sys import argv
    _CommandLine(argv)
