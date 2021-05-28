#!/usr/bin/python

from string import digits, ascii_uppercase

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


def _valid_num(value):
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


def _valid_bas(value):
    '''Returns an int with a value of 2 or above or
    raises InvalidBaseError exception.
    '''
    value = str(value).strip()

    if not value:
        value = DEFAULT_BASE

    try:
        # nominal case
        int_value = int(value)
    except ValueError:
        raise InvalidBaseError
    else:
        if MINIMUM_BASE <= int_value:
            # nominal case
            return int_value
        else:
            raise InvalidBaseError


def _val_to_char(input_num):
    try:
        input_num = int(input_num)
    except ValueError:
        raise InvalidInternalValueError

    # Negative indexes count backwards from the end of the list
    if input_num < 0:
        raise InvalidInternalValueError

    try:
        return ALLOWED_SYMBOLS[input_num]
    except IndexError:
        raise InvalidInternalValueError


def into_dec(in_num, in_bas):
    '''Returns an int.
    '''
    in_num = _valid_num(in_num)
    in_bas = _valid_bas(in_bas)
    try:
        return int(in_num, in_bas)
    except ValueError:
        raise InvalidInputBaseError


def from_dec(in_num, out_bas):
    '''Is an error for inNum to not be an integer.
    '''
    try:
        in_num = int(_valid_num(in_num))
    except ValueError:
        raise InvalidNumberError

    out_bas = _valid_bas(out_bas)

    minused = in_num < 0
    if minused:
        in_num *= -1

    values = []
    while (0 < in_num):
        values.append(_val_to_char(in_num % out_bas))
        in_num //= out_bas

    value = ''.join(reversed(values))

    if value:
        return (MINUS_SIGN * minused) + value
    else:
        return ZERO


def bas_calc(in_num, in_bas=DEFAULT_BASE, out_bas=DEFAULT_BASE):
    '''Given a number and its current base, returns the number with a
    new specified base.
    If a base is not given it is assumed to be base %d.
    ''' % (DEFAULT_BASE)
    return from_dec(into_dec(in_num, in_bas), out_bas)


def _command_line(args):
    if 1 < len(args):
        for arg in args[1:]:
            if arg in ('-h', '--help'):
                print('This program converts integers which may be signed ' +
                      'between any two number bases %d and over.\n' +
                      'Inputs as follows:\n' +
                      'in_num = the Input Number\n' +
                      'in_bas = the Input Base\n' +
                      'out_bas = the Output Base' % (MINIMUM_BASE))
                break
        else:
            print(bas_calc(*args[1:]))
    else:
        print('Base Converter')
        exit_vals = ('q', 'quit')
        exit_prompt = '\nEnter any of the following values to exit: %s\nor press return to continue: ' % str(exit_vals)
        while True:
            try:
                print('Output Number: ' +
                      bas_calc(
                          input('\nEnter an Input Number: ').strip(),
                          input('Enter an Input Base: ').strip(),
                          input('Enter an Output Base: ').strip()))
            except (BaseConvError, ValueError) as e:
                print('Error: ', e)
            if input(exit_prompt).strip().lower() in exit_vals:
                break


if __name__ == "__main__":
    from sys import argv
    _command_line(argv)
