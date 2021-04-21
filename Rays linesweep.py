import pygame
from Objects import Line
from random import seed, randint
from time import perf_counter as clock
from Rays import Particle

def createLines(amount):
    """Creates a set amount of random lines"""
    lines = list()
    for i in range(amount):
        start = (randint(0, 960), randint(0, 540))
        end = (randint(start[0] - 100, start[0] + 100), randint(start[1] - 100, start[1] + 100))
        if end[0] < start[0]:
            temp = start
            start = end
            end = temp
        lines.append(Line(start, end))
    return lines

def createSquareLines(amount):
    """Creates lines in a square fashion not completely random"""
    size = 60
    X = list(range(0, 960, size))
    Y = list(range(0, 540, size))
    lines = list()
    usedCords = list()
    while amount:
        if randint(0, 1):
            x = X[randint(0, len(X)-1)]
            y = Y[randint(0, len(Y)-1)]
            end = (x+size, y)
        else:
            x = X[randint(0, len(X)-1)]
            y = Y[randint(0, len(Y)-1)]
            end = (x, y+size)
        if (x, y) in usedCords:
            continue
        usedCords.append((x, y))
        amount -= 1
        start = (x, y)
        if end[0] < start[0]:
            temp = start
            start = end
            end = temp
        lines.append(Line(start, end))
    return lines

def Main():
    seed(1)
    pygame.init()
    pygame.font.init()
    Display = pygame.display.set_mode((960, 540))
    pygame.display.set_caption("Ray Casting")

    lines = createSquareLines(100)
    angle = [0, 360]
    particle = Particle(120, angle)

    distance = 200

    vertexDetectionToggle = False
    while True:
        then = clock()
        Display.fill((0, 0, 0))

        outlinePoints, hitInfo = particle.Emit(pygame.mouse.get_pos(), distance, lines, vertexDetection=vertexDetectionToggle)

        if pygame.mouse.get_pressed(3)[0]:
            for hit in hitInfo:
                if hit["extra"]:
                    pygame.draw.aaline(Display, (0, 0, 255), hit["ray"].start.ReturnList(), hit["point"].ReturnList(), 3)
                elif hit["hit"]:
                    pygame.draw.aaline(Display, (0, 255, 0), hit["ray"].start.ReturnList(), hit["point"].ReturnList(), 3)
                else:
                    pygame.draw.aaline(Display, (255, 0, 0), hit["ray"].start.ReturnList(), hit["point"].ReturnList(), 3)

        # Draw lines
        for line in lines:
            pygame.draw.aaline(Display, (255, 255, 255), line.start.ReturnList(), line.end.ReturnList())

        # Draw all the collision points and join them together
        pygame.draw.lines(Display, (255, 0, 0), True, outlinePoints, 3)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if vertexDetectionToggle:
                        vertexDetectionToggle = False
                    else:
                        vertexDetectionToggle = True
        pygame.display.update()
        print(1 / (clock() - then))


if __name__ == '__main__':
    Main()
