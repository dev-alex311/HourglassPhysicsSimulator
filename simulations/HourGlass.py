import sys
import random
import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
import numpy as np
from tkinter import *

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
    # plt.semilogy(x, y, 'ro', label='data')
    x_range = np.linspace(x[0], x[-1], 1000)
    # plt.semilogy(x_range, y_spl(x_range))
    y_spl_2d = y_spl.derivative(n=2)
    plt.plot(x_range, y_spl_2d(x_range), linestyle='none')

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
    plt.show()


def selPS():
    selection = "Value = " + str(particleSize.get())
    labelPartSizeValue.config(text=selection)


def selPM():
    selection = "Value = " + str(particleMass.get())
    labelPartMassValue.config(text=selection)


def selPA():
    selection = "Value = " + str(particleAmount.get())
    labelPartAmtValue.config(text=selection)


def selFH():
    selection = "Value = " + str(funnelHeight.get())
    labelFunHeightValue.config(text=selection)


def selFR():
    selection = "Value = " + str(funnelRadius.get())
    labelFunRadiusValue.config(text=selection)


def selAllVariables():
    global amountofballs
    global mass
    global radius
    global bodyheight
    global bodyradius

    radius = particleSize.get()
    mass = particleMass.get()
    amountofballs = particleAmount.get()
    bodyheight = funnelHeight.get()
    bodyradius = funnelRadius.get()

    labelPartSizeValue.config(text="Value = " + str(particleSize.get()))
    labelPartMassValue.config(text="Value = " + str(particleMass.get()))
    labelPartAmtValue.config(text="Value = " + str(particleAmount.get()))
    labelFunHeightValue.config(text="Value = " + str(funnelHeight.get()))
    labelFunRadiusValue.config(text="Value = " + str(funnelRadius.get()))

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
    pop = 0
    for i in range(amountofballs):
        ra = random.randint(250, 350)
        pop += ra

    ballsxposition.append(pop)
    ballstimeposition = []
    ballstimeposition.append(pygame.time.get_ticks())

    temp = 0
    balltimecount = 0
    firsttime = 0
    sleeptime = 5
    done = False

    for i in range(amountofballs):
        ball_shape = add_ball(space)
        balls.append(ball_shape)
    space.debug_draw(draw_options)

    while not done:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    done = True

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
    pygame.display.iconify()
    printballdata(ballsxposition, ballstimeposition)
    pygame.display.quit()

    sys.exit()

# window controls
window = Tk()
window.title("Hourglass Controls")
window.geometry("600x500")

# frame settings
framePartSize = Frame(window)
framePartSize.grid(row=0, sticky=W)

frameBuffer = Frame(window, height=25, width=600)
frameBuffer.grid(row=1)

framePartMass = Frame(window)
framePartMass.grid(row=2, sticky=W)

frameBuffer2 = Frame(window, height=25, width=600)
frameBuffer2.grid(row=3)

framePartAmt = Frame(window)
framePartAmt.grid(row=4, sticky=W)

frameBuffer3 = Frame(window, height=25, width=600)
frameBuffer3.grid(row=5)

frameFunHeight = Frame(window)
frameFunHeight.grid(row=6, sticky=W)

frameBuffer4 = Frame(window, height=25, width=600)
frameBuffer4.grid(row=7)

frameFunRadius = Frame(window)
frameFunRadius.grid(row=8, sticky=W)

frameBuffer4 = Frame(window, height=25, width=600)
frameBuffer4.grid(row=9)

frameButtons = Frame(window)
frameButtons.grid(row=10, sticky=W)
# widget code below

# label for particle size
part_size_string = StringVar()
labelTitlePartSize = Label(framePartSize, textvariable=part_size_string, width=15, anchor=W)
part_size_string.set("Particle Size:")

# slider and button for particle size
particleSize = DoubleVar()
scalePartSize = Scale(framePartSize, variable=particleSize, from_=1, to=25, orient=HORIZONTAL, length=300)
buttonPartSizeValue = Button(framePartSize, text="Get Value", command=selPS)
labelPartSizeValue = Label(framePartSize, text="Value = 10.0")
scalePartSize.set(10)

# label for particle mass
particleMass = DoubleVar()
part_mass_string = StringVar()
labelTitlePartMass = Label(framePartMass, textvariable=part_mass_string, width=15, anchor=W)
part_mass_string.set("Particle Mass:")

# slider and button for particle mass
scalePartMass = Scale(framePartMass, variable=particleMass, from_=1, to=500, orient=HORIZONTAL, length=300)
buttonPartMassValue = Button(framePartMass, text="Get Value", command=selPM)
labelPartMassValue = Label(framePartMass, text="Value = 15.0")
scalePartMass.set(15)

# label for particle amount
part_amt_string = StringVar()
labelTitlePartAmt = Label(framePartAmt, textvariable=part_amt_string, width=15, anchor=W)
part_amt_string.set("Particle Amount:")

# slider and button for particle amount
particleAmount = IntVar()
scalePartAmt = Scale(framePartAmt, variable=particleAmount, from_=1, to=500, orient=HORIZONTAL, length=300)
buttonPartAmtValue = Button(framePartAmt, text="Get Value", command=selPA)
labelPartAmtValue = Label(framePartAmt, text="Value = 75")
scalePartAmt.set(75)

# label for funnel height
funnel_height_string = StringVar()
labelTitleFunnelHeight = Label(frameFunHeight, textvariable=funnel_height_string, width=15, anchor=W)
funnel_height_string.set("Hourglass Height:")

# slider and button for funnel height
funnelHeight = DoubleVar()
scaleFunHeight = Scale(frameFunHeight, variable=funnelHeight, from_=0, to=200, orient=HORIZONTAL, length=300)
buttonFunHeightValue = Button(frameFunHeight, text="Get Value", command=selFH)
labelFunHeightValue = Label(frameFunHeight, text="Value = 100.0")
scaleFunHeight.set(100)

# label for funnel radius
funnel_radius_string = StringVar()
labelTitleFunnelRadius = Label(frameFunRadius, textvariable=funnel_radius_string, width=15, anchor=W)
funnel_radius_string.set("Hourglass Radius:")

# slider and button for funnel radius
funnelRadius = DoubleVar()
scaleFunRadius = Scale(frameFunRadius, variable=funnelRadius, from_=1, to=100, orient=HORIZONTAL, length=300)
buttonFunRadiusValue = Button(frameFunRadius, text="Get Value", command=selFR)
labelFunRadiusValue = Label(frameFunRadius, text="Value = 25.0")
scaleFunRadius.set(25)

# insert into framePartSize
labelTitlePartSize.grid(row=0, column=0, sticky=S)
scalePartSize.grid(row=0, column=2)
buttonPartSizeValue.grid(row=0, column=3, sticky=S)
labelPartSizeValue.grid(row=0, column=4, sticky=S)

# insert into framePartMass
labelTitlePartMass.grid(row=0, column=0, sticky=S)
scalePartMass.grid(row=0, column=2)
buttonPartMassValue.grid(row=0, column=3, sticky=S)
labelPartMassValue.grid(row=0, column=4, sticky=S)

# insert into framePartAmt
labelTitlePartAmt.grid(row=0, column=0, sticky=S)
scalePartAmt.grid(row=0, column=2)
buttonPartAmtValue.grid(row=0, column=3, sticky=S)
labelPartAmtValue.grid(row=0, column=4, sticky=S)

# insert into frameFunHeight
labelTitleFunnelHeight.grid(row=0, column=0, sticky=S)
scaleFunHeight.grid(row=0, column=2)
buttonFunHeightValue.grid(row=0, column=3, sticky=S)
labelFunHeightValue.grid(row=0, column=4, sticky=S)

# insert into frameFunRadius
labelTitleFunnelRadius.grid(row=0, column=0, sticky=S)
scaleFunRadius.grid(row=0, column=2)
buttonFunRadiusValue.grid(row=0, column=3, sticky=S)
labelFunRadiusValue.grid(row=0, column=4, sticky=S)

# button to collect all data
buttonAllValues = Button(frameButtons, text="Run Simulation", command=selAllVariables)
buttonAllValues.grid(row=1, column=0, sticky=E)

# begin Loop
window.mainloop()


