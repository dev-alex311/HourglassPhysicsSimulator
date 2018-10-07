import sys
import random
import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util

bodyheight = 0
mass = 0
radius = 0
bodyradius = 0
amountofballs = 0

def add_ball(space):
    global mass
    global radius
    mass = 5
    radius = 10
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, moment)
    x = random.randint(250, 350)
    y = random.randint(300 + bodyheight, 350 + bodyheight)
    body.position = x, y
    shape = pymunk.Circle(body, radius)
    space.add(body, shape)
    return shape


def add_hourglass(space):
    bodylefttriangle = pymunk.Body(body_type=pymunk.Body.STATIC)
    global bodyradius
    bodyradius = 50
    global bodyheight
    bodyheight = 200
    # change body1 and body2 x position to change the opening size
    bodylefttriangle.position = (245 - bodyradius, 150 + bodyheight)
    shape = pymunk.Poly(bodylefttriangle, [(0, 0), (0, 100), (50, 50)])
    space.add(shape)

    bodyrighttriangle = pymunk.Body(body_type=pymunk.Body.STATIC)
    # change body1 and body2 x position to change the opening size
    bodyrighttriangle.position = (355 + bodyradius, 150 + bodyheight)
    shape2 = pymunk.Poly(bodyrighttriangle, [(0, 0), (0, 100), (-50, 50)])
    space.add(shape2)

    bodybottom = pymunk.Body(body_type=pymunk.Body.STATIC)
    bodybottom.position = (200, 50)
    bb1 = pymunk.Segment(bodybottom, (-200, 0), (500, 0), 10)
    # change these 2 to change the opening
    bb2 = pymunk.Segment(bodybottom, (45 - bodyradius, 0), (45 - bodyradius, 350 + bodyheight), 10)
    bb3 = pymunk.Segment(bodybottom, (155 + bodyradius, 0), (155 + bodyradius, 350 + bodyheight), 10)
    space.add(bb1)
    space.add(bb2)
    space.add(bb3)

    bodytop = pymunk.Body(body_type=pymunk.Body.STATIC)
    bodytop.position = (200, 500)
    bt1 = pymunk.Segment(bodytop, (-200, -100 + bodyheight), (500, -100 + bodyheight), 10)
    space.add(bt1)

    return shape, shape2, bb1, bb2, bb3, bt1


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Hourglass Simulation")
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0.0, -900.0)
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    hg = add_hourglass(space)
    space.debug_draw(draw_options)
    balls = []
    global amountofballs
    amountofballs = 100
    for i in range(amountofballs):
        ball_shape = add_ball(space)
        balls.append(ball_shape)
    space.debug_draw(draw_options)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.display.quit()
                pygame.quit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.display.quit()
                    pygame.quit()

        space.step(1/80)
        screen.fill((255, 255, 255))
        space.debug_draw(draw_options)
        pygame.display.flip()
        clock.tick(25)

if __name__ == '__main__':
    main()
