from dataclasses import dataclass
import this

@dataclass
class Vector:
    x: int
    y: int


    def __add__(self, other):
        return (self.x + other.x), (self.y + other.y)

    def __repr__(self):
        return f"x: {self.x}, y: {self.y}"




x = Vector(3, 5)
y = Vector(1, 2)

ret = x + y
print(bool(ret))
