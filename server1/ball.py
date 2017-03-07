from random import *


class Vector:
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y)

    def __len__(self):
        return (self.x**2 + self.y**2)**0.5

    def cut(self):
        lensqr = self.x**2+self.y**2
        if (lensqr>1):
            length = lensqr**0.5
            return Vector(self.x/length,self.y/length)
        return self

class Point:
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y

    def __add__(self, other:Vector):
        return Point(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Vector(self.x-other.x, self.y-other.y)

    @classmethod
    def random(classs, width:float, height:float):
        return classs(randrange(1,width), randrange(1,height))



class Ball:
    def __init__(self, position:Point, speed:Vector, size:float):
        self.position = position
        self.speed = speed
        self.size = size

    @classmethod
    def random(classs, width:float, height:float, size:float):
        position = Point.random(width, height)
        speed = Vector(0,0)
        size = size
        return classs(position, speed, size)



    def move(self):
        self.speed = self.speed.cut()
        self.position = self.position + self.speed




def testBall(printing = False):
    myBall = Ball(Point(1,3), Vector(0,2), 3)
    myBall.move()
    if printing: print(myBall.position.y, "== 4.0")
    if printing: print(Ball.random(2000, 1000, 5).position.x, "== random")
    return myBall


if __name__ == '__main__':
    testBall(True)
