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

    def __mul__(self, scalar:int):
        return Vector(self.x*scalar, self.y*scalar)

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
        if isinstance(other, Vector):
            return Point(self.x-other.x, self.y-other.y)
        else:
            return Vector(self.x-other.x, self.y-other.y)

    def __mul__(self, scalar:int):
        return Point(self.x*scalar, self.y*scalar)

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
        self.moveDirection = Vector(0,0)  #no JSON
        self.gravity = 500  #100 ist Maximum


    @classmethod
    def random(classs, width:float, height:float, size:float, color="#FF00FF"):
        position = Point.random(width, height)
        speed = Vector(0,0)
        size = size
        return classs(position, speed, size, color)

    def getRadius(self):
        return self.size**0.5

    def move(self):
        self.gravity = min(500, self.gravity+1)
        self.speed += self.moveDirection
        self.speed *= 0.5

        self.position = (self.position + self.speed).cut(WIDTH, HEIGHT)

    def moveCommand(self, direction:Vector):
        self.moveDirection=direction.cut()

    def split(self):
        backPos = self.position + self.speed.cut()*(1/SPEED)*self.getRadius()*-0.5
        frontPos = self.position + self.speed.cut()*(1/SPEED)*self.getRadius()*1.5
        ballBack = Ball(backPos, self.speed, self.size/2, self.color)
        ballFront = Ball(frontPos, self.speed*10, self.size/2, self.color)
        ballBack.gravity = -200
        ballFront.gravity = -200
        return (ballBack, ballFront)

    def gravityTo(self, midpoint:Point):
        if (self.gravity < 0):
            return
        dist = midpoint - self.position
        dist = dist * (self.gravity / 10000.0)
        self.position = (self.position + dist).cut(WIDTH, HEIGHT)


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
