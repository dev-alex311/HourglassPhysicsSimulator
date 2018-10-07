import sys
import random
import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
import numpy as np

bodyheight = 0
mass = 0
radius = 0
bodyradius = 0
amountofballs = 0

def add_ball(space):
    global mass
    global radius
    global bodyheight

    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, moment)
    x = random.randint(250, 350)
    y = random.randint(300 + bodyheight, 350 + bodyheight)
    body.position = x, y
    shape = pymunk.Circle(body, radius)
    space.add(body, shape)
    return shape


def add_hourglass(space):
    global bodyradius
    global bodyheight

    bodylefttriangle = pymunk.Body(body_type=pymunk.Body.STATIC)
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


def printballdata(ballx, balltime):
    global mass
    global amountofballs

    totalmass = amountofballs * mass
    force = []
    g = -9.81
    x = np.array(balltime)
    y = np.array(ballx)

    y_spl = UnivariateSpline(x, y, s=0, k=4)
    plt.semilogy(x, y, 'ro', label='data')
    x_range = np.linspace(x[0], x[-1], 1000)
    plt.semilogy(x_range, y_spl(x_range))
    #y_spl_2d = y_spl.derivative(n=2)
    #plt.plot(x_range, y_spl_2d(x_range), linestyle='none')
    '''''
    line = plt.gca().get_lines()
    yd = line[0].get_ydata()
    xd = line[0].get_xdata()

    for i in range(len(yd)):
        force.append((totalmass*g)-(totalmass * (g + (mass/float(totalmass)*yd[i]))))

    forceprime = np.array(force)
    xprime = np.array(xd)
    force_spl = UnivariateSpline(xprime, forceprime, s=0, k=4)
    xrange1 = np.linspace(xprime[0], xprime[-1], 1000)
    plt.plot(xrange1, force_spl(xrange1))

    plt.ylabel(" Change in force ")
    plt.xlabel('time (milliseconds)')
    '''
    plt.show()


def main():
    global amountofballs
    global mass
    global radius
    global bodyheight
    global bodyradius

    amountofballs = 100
    bodyradius = 50
    bodyheight = 150
    mass = 50
    radius = 10

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
    ballsxposition = []
    ballsxposition.append(amountofballs*325)
    ballstimeposition = []
    ballstimeposition.append(0.0)
    temp = 0
    balltimecount = 0
    firsttime = 0
    sleeptime = 5

    for i in range(amountofballs):
        ball_shape = add_ball(space)
        balls.append(ball_shape)
    space.debug_draw(draw_options)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                printballdata(ballsxposition, ballstimeposition)
                pygame.display.quit()
                pygame.quit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    printballdata(ballsxposition, ballstimeposition)
                    pygame.display.quit()
                    pygame.quit()

        sleeptime -= 1
        # body.position.x and .y give different results
        if sleeptime <= 0:
            for i in range(amountofballs):
                for j in range(amountofballs):
                    temp += balls[j].body.position.x
                if firsttime == 0 or ballstimeposition[balltimecount] != pygame.time.get_ticks():
                    ballsxposition.append(temp)
                    ballstimeposition.append(pygame.time.get_ticks())
                    balltimecount += 1
                    firsttime += 1
                temp = 0
            sleeptime = 10

        space.step(1/80)
        screen.fill((255, 255, 255))
        space.debug_draw(draw_options)
        pygame.display.flip()
        clock.tick(25)


if __name__ == '__main__':
    main()
