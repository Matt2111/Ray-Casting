from Vectors import Vector

class Line:
    def __init__(self, start, end):
        self.start, self.end = Vector(*start), Vector(*end)

    def intersects(self, otherLine):
        selfDifference = Vector.MinusVectors(self.start, self.end)
        lineDifference = Vector.MinusVectors(otherLine.start, otherLine.end)
        denominator = selfDifference.x * lineDifference.y - selfDifference.y * lineDifference.x
        if not denominator:
            return
        t = ((self.start.x - otherLine.start.x) * lineDifference.y - (
                    self.start.y - otherLine.start.y) * lineDifference.x) / denominator
        u = -(selfDifference.x * (self.start.y - otherLine.start.y) - selfDifference.y * (
                    self.start.x - otherLine.start.x)) / denominator
        if 0 <= t <= 1 and 0 <= u <= 1:
            return Vector(self.start.x + -(t * selfDifference.x), self.start.y + -(t * selfDifference.y))
