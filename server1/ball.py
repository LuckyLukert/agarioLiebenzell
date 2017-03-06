
class Point:
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

class Vector:
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y


class Ball:
    def __init__(self, position:Point, speed:Vector, size:int):
        self.position = position
        self.speed = speed
        self.size = size


def testBall(printing = False):
    myBall = Ball(Point(1,2), Vector(0,1), 3)
    if printing: print(myBall.speed.y)
    return myBall

if __name__ == '__main__':
    testBall(True)
