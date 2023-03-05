import pygame, math


width = 800
height = 400
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# 1 METEER = 400PX
scale = 400
axis = (width / 2, 100)
radius = 5

g = 9.8

R1 = 0.2
R2 = 0.2

t = 0
dt = 0.01


class Bob:
    def __init__(self, theta, m, R, axis):
        self.theta = theta
        self.thetadt = 0
        self.m = m
        self.R = R
        self.x = R * math.sin(self.theta) * scale + axis[0]
        self.y = R * math.cos(self.theta) * scale + axis[1]
        self.axis = axis

    def draw(self):
        pygame.draw.lines(screen, (50, 50, 50), False, (self.axis, (self.x, self.y)))
        pygame.draw.circle(screen, (100, 100, 100), (self.x, self.y), radius)


def update():
    p1.draw()
    p2.draw()
    pygame.display.update()
    screen.fill((255, 255, 255))


p1 = Bob(math.pi / 4, 0.05, R1, axis)
p2 = Bob(math.pi / 4, 0.05, R2, (p1.x, p1.y))

theta1ddt = 0
theta2ddt = 0

while True:
    clock.tick(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    theta1ddt = -(R2*p2.m*math.sin(p1.theta-p2.theta)*p2.thetadt**2 + R2*p2.m*math.cos(p1.theta-p2.theta)*theta2ddt + g*p1.m*math.sin(p1.theta) + g*p2.m*math.sin(p1.theta)) / (R1*(p1.m+p2.m))

    theta2ddt = (R1*math.sin(p1.theta-p2.theta)*p1.thetadt**2 - R1*math.cos(p1.theta-p2.theta)*theta1ddt - g*math.sin(p2.theta)) / R2

    p1.thetadt += theta1ddt * dt
    p2.thetadt += theta2ddt * dt

    p1.theta += p1.thetadt * dt
    p2.theta += p2.thetadt * dt

    p1.x = R1 * math.sin(p1.theta) * scale + p1.axis[0]
    p1.y = R1 * math.cos(p1.theta) * scale + p1.axis[1]

    p2.axis = [p1.x, p1.y]
    p2.x = R2 * math.sin(p2.theta) * scale + p2.axis[0]
    p2.y = R2 * math.cos(p2.theta) * scale + p2.axis[1]

    t += dt

    update()
