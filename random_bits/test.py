class Shape:
    def move(self, dx, dy):
        raise NotImplemented()


class Point(Shape):
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y

    def __str__(self):
        return f'Point [x = {self.x}, y = {self.y}]'

    def move(self, dx, dy):
        return Point(self.x + dx, self.y + dy)


class Rectangle(Shape):
    def __init__(self, ll: Point, tr: Point):
        self.ll = ll
        self.tr = tr

    def __str__(self):
        return f'Rectangle: [ll: {self.ll}, tr: {self.tr}]'

    def move(self, dx, dy):
        return Rectangle(self.ll.move(dx, dy), self.tr.move(dx, dy))


class Circle(Shape):
    def __init__(self, center: Point, radius: int):
        self.center = center
        self.radius = radius

    def move(self, dx, dy):
        return Circle(self.center.move(dx, dy), self.radius)

    def __str__(self):
        return f'Circle: [center: {self.center}, radius: {self.radius}'


p1 = Point(1, 1)

p2 = p1.move(10, 10)

r1 = Rectangle(p1, p2)
r2 = r1.move(10, 20)

c1 = Circle(p1, 10)
c2 = Circle(p2, 20)

shapes = [p1, p2, r1, r2, c1, c2]

# print([str(s) for s in shapes])
print([str(s.move(10, 10)) for s in shapes])
