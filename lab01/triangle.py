import sys


EXIT_FAILURE = 1

MIN_LENGTH = 1
MAX_LENGTH = 4294967295

SCALENE = 'обычный'
ISOSCELES = 'равнобедренный'
EQUILATERAL = 'равносторонний'
NOT_TRIANGLE = 'не треугольник'
ERROR = 'неизвестная ошибка'


def validate_values(*values):
    for value in values:
        if value < MIN_LENGTH or value > MAX_LENGTH:
            return False

    return True


def is_triangle(a, b ,c):
    return (a + b > c) and (b + c > a) and (a + c > b)


def is_equilateral_triangle(a, b ,c):
    if not is_triangle(a, b, c):
        return False

    return (a == b) and (b == c)


def is_isosceles_triangle(a, b ,c):
    if not is_triangle(a, b, c):
        return False

    return (a == b and b != c) or (a == c and c != b) or (b == c and c != a)


def main(args):
    if len(args) != 3:
        print(ERROR)
        sys.exit(EXIT_FAILURE)

    try:
        a = float(args[0])
        b = float(args[1])
        c = float(args[2])
    except ValueError:
        print(ERROR)
        sys.exit(EXIT_FAILURE)

    if not validate_values(a, b, c):
        print(NOT_TRIANGLE)
        sys.exit(EXIT_FAILURE)

    if is_equilateral_triangle(a, b, c):
        print(EQUILATERAL)
    elif is_isosceles_triangle(a, b, c):
        print(ISOSCELES)
    elif is_triangle(a, b, c):
        print(SCALENE)
    else:
        print(NOT_TRIANGLE)


if __name__ == '__main__':
    main(sys.argv[1:])
