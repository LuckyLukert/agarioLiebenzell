
class Point:
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y

class Vector:
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y

    def cut(self):
        lensqr = self.x**2+self.y**2
        if (lensqr>1):
            length = lensqr**0.5
            return Vector(self.x/length,self.y/length)
        return self


class Ball:
    def __init__(self, position:Point, speed:Vector, size:float):
        self.position = position
        self.speed = speed
        self.size = size

    def move(self):
        self.speed = self.speed.cut()
        self.position = Point(self.position.x + self.speed.x, self.position.y + self.speed.y)


def testBall(printing = False):
    myBall = Ball(Point(1,3), Vector(0,2), 3)
    myBall.move()
    if printing: print(myBall.position.y, "== 4.0")

    return myBall

if __name__ == '__main__':
    testBall(True)
