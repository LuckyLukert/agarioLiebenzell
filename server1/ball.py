from random import *
from settings import *


class Vector:
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y

    @classmethod
    def byJSON(cls, entries):
        v = cls(0,0)
        v.__dict__.update(entries)
        return v

    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y)

    def length(self):
        return (self.x**2 + self.y**2)**0.5

    def cut(self):
        lensqr = self.x**2+self.y**2
        if (lensqr>SPEED):
            length = lensqr**0.5
            return Vector(SPEED*self.x/length,SPEED*self.y/length)
        return self

    def reprJSON(self):
        return self.__dict__.copy()


class Point:
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y

    def __add__(self, other:Vector):
        return Point(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Vector(self.x-other.x, self.y-other.y)

    def cut(self, width, height):
        return Point(max(0.0, min(self.x, width)), max(0.0, min(self.y, height)))

    @classmethod
    def random(classs, width:float, height:float):
        return classs(randrange(1,width), randrange(1,height))


    def reprJSON(self):
        return self.__dict__.copy()


class Ball:
    def __init__(self, position:Point, speed:Vector, size:float, color="#FF00FF"):
        self.position = position
        self.speed = speed
        self.size = size
        self.color = color


    @classmethod
    def random(classs, width:float, height:float, size:float):
        position = Point.random(width, height)
        speed = Vector(0,0)
        size = size
        return classs(position, speed, size)


    def move(self):
        self.speed = self.speed.cut()
        self.position = (self.position + self.speed).cut(WIDTH, HEIGHT)


    def reprJSON(self):
        return self.__dict__.copy()


def testBall(printing = False):
    myBall = Ball(Point(1,3), Vector(0,2), 3)
    myBall.move()
    if printing: print(myBall.position.y, "== 4.0")
    if printing: print(Ball.random(2000, 1000, 5).position.x, "== random")
    return myBall


if __name__ == '__main__':
    testBall(True)
