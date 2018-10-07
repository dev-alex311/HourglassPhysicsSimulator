import sys
import random
import math
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
angle = 0


def add_ball(space):
    global mass
    global radius
    global bodyheight

    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, moment)
    x = random.randint(275, 325)
    y = random.randint(250 + bodyheight, 300 + bodyheight)
    body.position = x, y
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0.0
    shape.friction = 10.0
    space.add(body, shape)
    return shape


def add_hourglass(space):
    global bodyradius
    global bodyheight
    global angle

    bodylefttriangle = pymunk.Body(body_type=pymunk.Body.STATIC)
    # change body1 and body2 x position to change the opening size
    bodylefttriangle.position = (245 - bodyradius, 150 + bodyheight)
    shape = pymunk.Poly(bodylefttriangle, [(0, 50), (0, 50 + angle), (50, 50)])
    shape.elasticity = 0.0
    shape.friction = 0
    space.add(shape)

    bodyrighttriangle = pymunk.Body(body_type=pymunk.Body.STATIC)
    # change body1 and body2 x position to change the opening size
    bodyrighttriangle.position = (355 + bodyradius, 150 + bodyheight)
    shape2 = pymunk.Poly(bodyrighttriangle, [(0, 50), (0, 50 + angle), (-50, 50)])
    shape2.elasticity = 0.0
    shape2.friction = 0
    space.add(shape2)

    bodybottom = pymunk.Body(body_type=pymunk.Body.STATIC)
    bodybottom.position = (200, 50)
    bb1 = pymunk.Segment(bodybottom, (-200, 0), (500, 0), 10)
    # change these 2 to change the opening
    bb2 = pymunk.Segment(bodybottom, (45 - bodyradius, 0), (45 - bodyradius, 350 + bodyheight), 10)
    bb3 = pymunk.Segment(bodybottom, (155 + bodyradius, 0), (155 + bodyradius, 350 + bodyheight), 10)

    bb1.elasticity = 0.0
    bb2.elasticity = 0.0
    bb3.elasticity = 0.0
    bb1.friction = 10
    bb2.friction = 10
    bb3.friction = 10
    space.add(bb1)
    space.add(bb2)
    space.add(bb3)

    bodytop = pymunk.Body(body_type=pymunk.Body.STATIC)
    bodytop.position = (200, 500)
    bt1 = pymunk.Segment(bodytop, (-200, -100 + bodyheight), (500, -100 + bodyheight), 10)

    bt1.elasticity = 0.0
    bt1.friction = 100
    space.add(bt1)

    bodystop = pymunk.Body(body_type=pymunk.Body.STATIC)
    bodystop.position = (250 - bodyradius, 200 + bodyheight)
    bstopper = pymunk.Segment(bodystop, (0, 0), (120 + bodyradius, 0), 5)
    space.add(bstopper)

    return shape, shape2, bb1, bb2, bb3, bt1, bstopper


def printballdata(ballx, balltime):
    global mass
    global amountofballs

    totalmass = amountofballs * (mass)
    force = []

    ballxprime = []

    for i in ballx:
        ballxprime.append(i/1000)

    g = -9.81
    x = np.array(balltime)
    y = np.array(ballxprime)

    y_spl = UnivariateSpline(x, y, s=0, k=3)
    # plt.semilogy(x, y, 'ro', label='data')
    x_range = np.linspace(x[0], x[-1], 1000)
    # plt.semilogy(x_range, y_spl(x_range))
    y_spl_1d = y_spl.derivative(n=1)
    y_spl_2d = y_spl.derivative(n=2)
    plt.plot(x_range, y_spl_2d(x_range), linestyle='none')


    line = plt.gca().get_lines()
    yd = line[0].get_ydata()
    xd = line[0].get_xdata()

    for i in range(len(yd)):
        force.append((totalmass * 1000 * (g + ((mass*1000)/float(totalmass*1000)*(yd[i]*100))))-(totalmass*g*1000))

    forceprime = np.array(force)
    xprime = np.array(xd)
    force_spl = UnivariateSpline(xprime, forceprime, s=0, k=4)
    xrange1 = np.linspace(xprime[0], xprime[-1], 1000)

    plt.figure(1)
    plt.plot(x_range, y_spl(x_range))
    plt.ylabel("Distance (cm)")
    plt.xlabel('time (milliseconds)')
    plt.figure(2)
    plt.plot(x_range, y_spl_1d(x_range))
    plt.ylabel("Velocity ")
    plt.xlabel('time (milliseconds)')
    plt.figure(3)
    plt.plot(xrange1, force_spl(xrange1))
    plt.ylabel("Change in force (N)")
    plt.xlabel('time (milliseconds)')
    plt.show()


def selPS():
    selection = "Value = " + str(particleSize.get()) + " cm"
    labelPartSizeValue.config(text=selection)


def selPM():
    selection = "Value = " + str(particleMass.get()) + " g"
    labelPartMassValue.config(text=selection)


def selPA():
    selection = "Value = " + str(particleAmount.get())
    labelPartAmtValue.config(text=selection)


def selFH():
    selection = "Value = " + str(funnelHeight.get()) + " cm"
    labelFunHeightValue.config(text=selection)


def selFR():
    selection = "Value = " + str(funnelRadius.get()) + " cm"
    labelFunRadiusValue.config(text=selection)

def selTA():
    abdistance = math.sqrt(((0-50)**2)+((50-50)**2))
    acdistance = math.sqrt(((0-0)**2)+((50-(50+triangleAngle.get()))**2))
    bcdistance = math.sqrt(((50 - 0) ** 2) + ((50 - (50 + triangleAngle.get())) ** 2))
    cosB = ((bcdistance**2) + (abdistance**2) - (acdistance**2))/(2*bcdistance*abdistance)
    Bangle = math.degrees(math.acos(cosB))
    selection = "Value = " + str(triangleAngle.get()) + " Angle = " + str(round(Bangle, 1)) + "°"
    labelTriAngleValue.config(text=selection)


def selAllVariables():
    global amountofballs
    global mass
    global radius
    global bodyheight
    global bodyradius
    global angle

    radius = particleSize.get()
    mass = particleMass.get()
    amountofballs = particleAmount.get()
    bodyheight = funnelHeight.get()
    bodyradius = funnelRadius.get()
    angle = triangleAngle.get()

    abdistance = math.sqrt(((0-50)**2)+((50-50)**2))
    acdistance = math.sqrt(((0-0)**2)+((50-(50+triangleAngle.get()))**2))
    bcdistance = math.sqrt(((50 - 0) ** 2) + ((50 - (50 + triangleAngle.get())) ** 2))
    cosB = ((bcdistance**2) + (abdistance**2) - (acdistance**2))/(2*bcdistance*abdistance)
    Bangle = math.degrees(math.acos(cosB))

    labelPartSizeValue.config(text="Value = " + str(particleSize.get()) + " cm")
    labelPartMassValue.config(text="Value = " + str(particleMass.get()) + " g")
    labelPartAmtValue.config(text="Value = " + str(particleAmount.get()))
    labelFunHeightValue.config(text="Value = " + str(funnelHeight.get()) + " cm")
    labelFunRadiusValue.config(text="Value = " + str(funnelRadius.get()) + " cm")
    labelTriAngleValue.config(text="Value = " + str(triangleAngle.get()) + " Angle = " + str(round(Bangle, 1)) + "°")

    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Hourglass Simulation")
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0.0, -900.0)
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    hr = add_hourglass(space)
    space.debug_draw(draw_options)

    balls = []
    ballsxposition = []
    ballstimeposition = []

    pop = 0
    temp = 0
    balltimecount = 0
    firsttime = 0
    removed = 0
    removebegin = 100
    sleeptime = 100
    done = False

    for i in range(amountofballs):
        ball_shape = add_ball(space)
        balls.append(ball_shape)
    space.debug_draw(draw_options)

    space.debug_draw(draw_options)
    pygame.display.flip()
    pygame.time.delay(1000)

    while not done:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    done = True

        removebegin -= 1
        if removed == 0 and removebegin <= 0:
            #space.remove(hr[6], hr[6].body)
            for i in range(amountofballs):
                pop += balls[i].body.position.y
            ballsxposition.append(pop)
            ballstimeposition.append(pygame.time.get_ticks())
            space._remove_shape(hr[6])
            space.debug_draw(draw_options)
            removed += 1

        sleeptime -= 1
        # body.position.x and .y give different results!!!
        if sleeptime <= 0:
            for i in range(amountofballs):
                for j in range(amountofballs):
                    temp += balls[j].body.position.y
                if firsttime == 0 or ballstimeposition[balltimecount] != pygame.time.get_ticks():
                    ballsxposition.append(temp)
                    ballstimeposition.append(pygame.time.get_ticks())
                    balltimecount += 1
                    firsttime += 1
                temp = 0
            sleeptime = 50

        space.step(1/85)
        screen.fill((255, 255, 255))
        space.debug_draw(draw_options)
        pygame.display.flip()
        clock.tick(45)
    pygame.display.iconify()
    printballdata(ballsxposition, ballstimeposition)
    pygame.display.quit()

    sys.exit()

# window controls
window = Tk()
window.title("Hourglass Controls")
window.geometry("650x500")

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

frameTriAngle = Frame(window)
frameTriAngle.grid(row=10, sticky=W)

frameBuffer5 = Frame(window, height=25, width=600)
frameBuffer5.grid(row=11)

frameButtons = Frame(window)
frameButtons.grid(row=12, sticky=W)
# widget code below

# label for particle size
part_size_string = StringVar()
labelTitlePartSize = Label(framePartSize, textvariable=part_size_string, width=15, anchor=W)
part_size_string.set("Particle Size:")

# slider and button for particle size
particleSize = DoubleVar()
scalePartSize = Scale(framePartSize, variable=particleSize, from_=1, to=100, orient=HORIZONTAL, length=300, resolution=1)
buttonPartSizeValue = Button(framePartSize, text="Get Value", command=selPS)
labelPartSizeValue = Label(framePartSize, text="Value = 1 cm")
scalePartSize.set(1)

# label for particle mass
particleMass = DoubleVar()
part_mass_string = StringVar()
labelTitlePartMass = Label(framePartMass, textvariable=part_mass_string, width=15, anchor=W)
part_mass_string.set("Particle Mass:")

# slider and button for particle mass
scalePartMass = Scale(framePartMass, variable=particleMass, from_=1, to=1000, orient=HORIZONTAL, length=300, resolution=1)
buttonPartMassValue = Button(framePartMass, text="Get Value", command=selPM)
labelPartMassValue = Label(framePartMass, text="Value = 1 g")
scalePartMass.set(1)

# label for particle amount
part_amt_string = StringVar()
labelTitlePartAmt = Label(framePartAmt, textvariable=part_amt_string, width=15, anchor=W)
part_amt_string.set("Particle Amount:")

# slider and button for particle amount
particleAmount = IntVar()
scalePartAmt = Scale(framePartAmt, variable=particleAmount, from_=1, to=1000, orient=HORIZONTAL, length=300)
buttonPartAmtValue = Button(framePartAmt, text="Get Value", command=selPA)
labelPartAmtValue = Label(framePartAmt, text="Value = 100")
scalePartAmt.set(100)

# label for funnel height
funnel_height_string = StringVar()
labelTitleFunnelHeight = Label(frameFunHeight, textvariable=funnel_height_string, width=15, anchor=W)
funnel_height_string.set("Hourglass Height:")

# slider and button for funnel height
funnelHeight = DoubleVar()
scaleFunHeight = Scale(frameFunHeight, variable=funnelHeight, from_=0, to=200, orient=HORIZONTAL, length=300)
buttonFunHeightValue = Button(frameFunHeight, text="Get Value", command=selFH)
labelFunHeightValue = Label(frameFunHeight, text="Value = 50.0 cm")
scaleFunHeight.set(50)

# label for funnel radius
funnel_radius_string = StringVar()
labelTitleFunnelRadius = Label(frameFunRadius, textvariable=funnel_radius_string, width=15, anchor=W)
funnel_radius_string.set("Hourglass Radius:")

# slider and button for funnel radius
funnelRadius = DoubleVar()
scaleFunRadius = Scale(frameFunRadius, variable=funnelRadius, from_=1, to=25, orient=HORIZONTAL, length=300)
buttonFunRadiusValue = Button(frameFunRadius, text="Get Value", command=selFR)
labelFunRadiusValue = Label(frameFunRadius, text="Value = 5.0 cm")
scaleFunRadius.set(5)

# label for triangle angle
triangle_angle_string = StringVar()
labelTitleTriangleAngle = Label(frameTriAngle, textvariable=triangle_angle_string, width=15, anchor=W)
triangle_angle_string.set("Incline Shift:")

# slider and button for triangle angle
triangleAngle = DoubleVar()
scaleTriAngle = Scale(frameTriAngle, variable=triangleAngle, from_=0, to=280, orient=HORIZONTAL, length=300)
buttonTriAngleValue = Button(frameTriAngle, text="Get Value", command=selTA)
labelTriAngleValue = Label(frameTriAngle, text="Value = 50.0 Angle = 45.0°")
scaleTriAngle.set(50)

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

# insert into frameTriAngle
labelTitleTriangleAngle.grid(row=0, column=0, sticky=S)
scaleTriAngle.grid(row=0, column=2)
buttonTriAngleValue.grid(row=0, column=3, sticky=S)
labelTriAngleValue.grid(row=0, column=4, sticky=S)

# button to collect all data
buttonAllValues = Button(frameButtons, text="Run Simulation", command=selAllVariables)
buttonAllValues.grid(row=1, column=0, sticky=E)

# begin Loop
window.mainloop()


