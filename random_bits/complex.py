class Complex:
    def __init__(self, real, imaginary=0):
        self.real = real
        self.imaginary = imaginary

    def __add__(self, other):
        if type(other) is not Complex:
            other = Complex(other)

        return Complex(self.real + other.real,
                       self.imaginary + other.imaginary)

    def __radd__(self, other):
        return self + Complex(other)

    def __rmul__(self, other):
        return self * Complex(other)

    def __mul__(self, other):
        #  (3 + 2i)(1 + 4i)
        if type(other) is not Complex:
            other = Complex(other)

        return Complex(
            self.real * other.real - self.imaginary * other.imaginary,
            self.imaginary * other.real + self.real * other.imaginary)

    def __str__(self):
        return f'[{self.real} + {self.imaginary}i]'

    def __iter__(self):
        yield self.real
        yield self.imaginary


c1 = Complex(1, 1)
c2 = Complex(2, 2)

print(c1, c1, c1 * c2)

print(Complex(3, 2) * Complex(1, 4))

print(3 + c1)

print(3 * c1)

print(c1 * 3)

print(c1 + 3)

for i in c1:
    print(i)
