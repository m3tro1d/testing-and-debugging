import sys


EXIT_FAILURE = 1

SCALENE = 'обычный'
ISOSCELES = 'равнобедренный'
EQUILATERAL = 'равосторонний'
NOT_TRIANGLE = 'не треугольник'
ERROR = 'неизвестная ошибка'


def main(args):
    if len(args) != 3:
        print(ERROR)
        sys.exit(EXIT_FAILURE)

    a = args[0]
    b = args[1]
    c = args[2]

    if a == b == c:
        print(EQUILATERAL)
    elif a == b or b == c or a == c:
        print(ISOSCELES)
    else:
        print(SCALENE)


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('keyboard interrupt')
