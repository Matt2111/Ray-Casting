from Vectors import Vector
from Objects import Line

def CheckDistance(pointA, pointB):
    difference = Vector.MinusVectors(pointA, pointB)
    return difference.x*difference.x + difference.y*difference.y

class Ray:
    def __init__(self, point, direction, distance):
        self.start = Vector(point[0], point[1])
        self.direction = direction
        self.magnitude = Vector.DegreesToVector(direction, distance=distance)
        self.end = Vector.AddVectors(self.start, self.magnitude)
        self.collisions = list()
        self.collidedLine = None

    def CollideLine(self, line):
        selfDifference = Vector.MinusVectors(self.start, self.end)
        lineDifference = Vector.MinusVectors(line.start, line.end)
        denominator = selfDifference.x * lineDifference.y - selfDifference.y * lineDifference.x
        if not denominator:
            return
        t = ((self.start.x - line.start.x) * lineDifference.y - (self.start.y - line.start.y) * lineDifference.x)/denominator
        u = -(selfDifference.x * (self.start.y - line.start.y) - selfDifference.y * (self.start.x - line.start.x))/denominator
        if 0 <= t <= 1 and 0 <= u <= 1:
            collisionPoint = Vector(self.start.x + -(t * selfDifference.x), self.start.y + -(t * selfDifference.y))
            return collisionPoint, CheckDistance(self.start, collisionPoint), line

    def CollideLines(self, lines):
        return list(map(self.CollideLine, lines))

class Particle:
    def __init__(self, rayAmount, boundaries):
        self.boundaries = boundaries
        self.rayAmount = rayAmount

    def UpdateBoundaries(self, boundaries):
        self.boundaries = boundaries

    @staticmethod
    def createRLObjects(lines, rays):
        """Sorts the lines and rays based on y value for line-sweeping later"""
        rayLineObjects = list()
        for line in lines:
            rayLineObjects.append({"pos": line.start.y, "object": line, "type": "start"})
            rayLineObjects.append({"pos": line.end.y, "object": line, "type": "end"})
        for ray in rays:
            rayLineObjects.append({"pos": max(ray.start.y, ray.end.y), "object": ray, "type": "start"})
            rayLineObjects.append({"pos": min(ray.start.y, ray.end.y), "object": ray, "type": "end"})
        rayLineObjects.sort(key=lambda x: x["pos"], reverse=True)
        return rayLineObjects

    def EmitNoCollision(self, position, distance):
        degreeChange = (self.boundaries[1] - self.boundaries[0]) / self.rayAmount
        rays = [Ray(position, self.boundaries[0] + degreeChange * x, distance) for x in range(self.rayAmount)]
        return rays

    def Emit(self, position, distance, lines, vertexDetection=True):
        # Make 2 lists one for lines and one for rays to keep track of what line/ray is active so we can apply line-sweep
        activeLines = list()
        activeRays = list()

        # Generate some rays at the position specified
        degreeChange = (self.boundaries[1] - self.boundaries[0]) / self.rayAmount
        rays = [Ray(position, self.boundaries[0] + degreeChange * x, distance) for x in range(self.rayAmount)]

        # Sort the rays and lines based on y value ready for line sweeping
        rayLineObjects = self.createRLObjects(lines, rays)

        # Complete line sweeping
        for obj in rayLineObjects:
            # Separate lines from rays as they will be handled differently
            # If the current object is a line do:
            if isinstance(obj["object"], Line):
                # If we have the top of the line add it to the active lines list and cycle through the rays to see if
                # any collide with it
                if obj["type"] == "start":
                    newLine = obj["object"]
                    activeLines.append(newLine)
                    for ray in activeRays:
                        result = ray.CollideLine(newLine)
                        # If the ray does collide add the collision to the rays memory so we can check all of its
                        # collisions later
                        if result:
                            ray.collisions.append(result)
                # If we are at the lowest point of the line remove it from the active lines list
                else:
                    activeLines.remove(obj["object"])
            # If the current object is a ray do this:
            else:
                # If we are at the top of the ray add it to the activeRays list and collide it with all the active lines
                if obj["type"] == "start":
                    newRay = obj["object"]
                    # For every line in activeLines check if this ray collides with them
                    for result in newRay.CollideLines(activeLines):
                        # If it did collide add the collision to the rays memory so we can use it later
                        if result:
                            newRay.collisions.append(result)
                    activeRays.append(newRay)
                # If we are at the bottom of the ray remove it from the activeRays list
                else:
                    newRay = obj["object"]
                    activeRays.remove(newRay)

        # Make a list of all the points hit by rays
        outlinePoints = list()
        # Make a list of all the hits and their info including angle and distance squared
        hitInfo = list()
        # For each ray see if it collided and if it has choose the closest collision and add it to "outlinePoints"
        for ray in rays:
            # If ray has collided
            if ray.collisions:
                # Pick the closest collision by choosing the smallest squared distance
                closestCollision = min(ray.collisions, key=lambda _: _[1])
                ray.collidedLine = closestCollision[2]
                # Add the closest collision to the list
                outlinePoints.append(closestCollision[0].ReturnList())
                hitInfo.append({"angle": ray.direction, "distance": closestCollision[1], "extra": False, "ray": ray, "hit": True, "point": closestCollision[0]})

            else:
                outlinePoints.append(ray.end.ReturnList())
                hitInfo.append({"angle": ray.direction, "distance": CheckDistance(ray.start, ray.end), "extra": False, "ray": ray, "hit": False, "point": ray.end})

        if vertexDetection:
            # Changed is important so we can keep track of how the rays position change in the list
            changed = 0
            # Cycle through the rays in pairs
            for x in range(len(rays)-1):
                ray, otherRay = rays[x], rays[x + 1]
                # Skip this ray pair if they have hit the same line as we wont be able to get any more detail most likely
                if ray.collidedLine == otherRay.collidedLine:
                    continue
                # If both rays have collided we want to pick the closest line so we don't break through any other walls
                elif ray.collidedLine is not None and otherRay.collidedLine is not None:
                    # Get the closest lines distance from each
                    distRay = min(ray.collisions, key=lambda _: _[1])[1]
                    distOtherRay = min(otherRay.collisions, key=lambda _: _[1])[1]
                    # Here we make sure the ray hits are at least some difference away so we don't "break" a wall
                    # If there are rays "breaking" walls increase "wallDistance"
                    wallDistance = 250
                    if abs(distRay - distOtherRay) <= wallDistance:
                        continue
                    # Here we chose the closest wall and set the furthest wall to none
                    if distRay < distOtherRay:
                        otherRay.collidedLine = None
                    else:
                        ray.collidedLine = None

                result = None

                recentMidRay = None
                recentMidRayResult = None

                for i in range(5):
                    # Find the angle between the 2 rays so we can shine a new ray directly down the center
                    dirA, dirB = ray.direction, otherRay.direction
                    mid = dirA + abs(dirA - dirB) / 2
                    midRay = Ray(ray.start.ReturnList(), mid, distance)

                    # Make sure you chose a valid line
                    if otherRay.collidedLine is not None and ray.collidedLine is None:
                        result = midRay.CollideLine(otherRay.collidedLine)
                    elif otherRay.collidedLine is None and ray.collidedLine is not None:
                        result = midRay.CollideLine(ray.collidedLine)

                    # If the mid ray actually hit something make update the ray
                    if result is not None:
                        midRay.collidedLine = result[2]
                        recentMidRay = midRay
                        recentMidRayResult = result

                    # Zoom in on the vertex
                    if ray.collidedLine is not None and midRay.collidedLine is None:
                        otherRay = midRay
                    elif otherRay.collidedLine is not None and midRay.collidedLine is None:
                        ray = midRay
                    elif ray.collidedLine is not None and midRay.collidedLine is not None:
                        ray = midRay
                    elif otherRay.collidedLine is not None and midRay.collidedLine is not None:
                        otherRay = midRay

                # Add the new found vertex into the list of collision points
                if recentMidRayResult is not None:
                    result = recentMidRayResult
                    midRay = recentMidRay
                    outlinePoints.insert(x + 1 + changed, result[0].ReturnList())
                    hitInfo.insert(x + 1 + changed, {"angle": midRay.direction, "distance": result[1], "extra": True, "ray": midRay, "hit": True, "point": result[0]})
                    changed += 1  # Make  sure we take into the fact the list is changing sizes
        return outlinePoints, hitInfo
