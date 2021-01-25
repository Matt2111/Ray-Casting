from math import cos, sin, radians

class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def ReturnList(self):
        return [self.x, self.y]

    @staticmethod
    def DegreesToVector(angle, distance=1):
        angle = radians(angle)
        return Vector(cos(angle) * distance, sin(angle) * distance)

    @staticmethod
    def RadiansToVector(angle, distance=1):
        return Vector(cos(angle) * distance, sin(angle) * distance)

    @staticmethod
    def DotVectors(vectorA, vectorB):
        return vectorA.x * vectorB.x + vectorA.y * vectorB.y

    @staticmethod
    def AddVectors(vectorA, vectorB):
        return Vector(vectorA.x + vectorB.x, vectorA.y + vectorB.y)

    @staticmethod
    def MinusVectors(vectorA, vectorB):
        return Vector(vectorA.x - vectorB.x, vectorA.y - vectorB.y)

    def AddVector(self, otherVector):
        self.x += otherVector.x
        self.y += otherVector.y

    def MinusVector(self, otherVector):
        self.x -= otherVector.x
        self.y -= otherVector.y



