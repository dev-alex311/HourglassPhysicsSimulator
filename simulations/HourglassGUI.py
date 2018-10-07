from tkinter import *


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
    print(particleSize.get())
    print(particleMass.get())
    print(particleAmount.get())
    print(funnelHeight.get())
    print(funnelRadius.get())

    labelPartSizeValue.config(text="Value = " + str(particleSize.get()))
    labelPartMassValue.config(text="Value = " + str(particleMass.get()))
    labelPartAmtValue.config(text="Value = " + str(particleAmount.get()))
    labelFunHeightValue.config(text="Value = " + str(funnelHeight.get()))
    labelFunRadiusValue.config(text="Value = " + str(funnelRadius.get()))

#window controls
window = Tk()
window.title("Hourglass Controls")
window.geometry("600x500")


#frame settings
framePartSize = Frame(window)
framePartSize.grid(row=0, sticky=W)

frameBuffer = Frame(window, height=25, width=600)
frameBuffer.grid(row=1)

framePartMass = Frame(window)
framePartMass.grid(row=2,  sticky=W)

frameBuffer2 = Frame(window, height=25, width=600)
frameBuffer2.grid(row=3)

framePartAmt = Frame(window)
framePartAmt.grid(row=4,  sticky=W)

frameBuffer3 = Frame(window, height=25, width=600)
frameBuffer3.grid(row=5)

frameFunHeight = Frame(window)
frameFunHeight.grid(row=6,  sticky=W)

frameBuffer4 = Frame(window, height=25, width=600)
frameBuffer4.grid(row=7)

frameFunRadius = Frame(window)
frameFunRadius.grid(row=8,  sticky=W)

frameBuffer4 = Frame(window, height=25, width=600)
frameBuffer4.grid(row=9)

frameButtons = Frame(window)
frameButtons.grid(row=10, sticky=W)
#widget code below

#label for particle size
part_size_string = StringVar()
labelTitlePartSize = Label(framePartSize, textvariable=part_size_string, width=15, anchor=W)
part_size_string.set("Particle Size:")

#slider and button for particle size
particleSize = DoubleVar()
scalePartSize = Scale(framePartSize, variable=particleSize, from_=1, to=25, orient=HORIZONTAL, length=300)
buttonPartSizeValue = Button(framePartSize, text="Get Value", command=selPS)
labelPartSizeValue = Label(framePartSize, text="Value = 5.0")
scalePartSize.set(5)

#label for paricle mass
part_mass_string = StringVar()
labelTitlePartMass = Label(framePartMass, textvariable=part_mass_string, width=15, anchor=W)
part_mass_string.set("Particle Mass:")

#slider and button for particle mass
particleMass = DoubleVar()
scalePartMass = Scale(framePartMass, variable=particleMass, from_=1, to=500, orient=HORIZONTAL, length=300)
buttonPartMassValue = Button(framePartMass, text="Get Value", command=selPM)
labelPartMassValue = Label(framePartMass, text="Value = 5.0")
scalePartMass.set(5)

#label for paricle amount
part_amt_string = StringVar()
labelTitlePartAmt = Label(framePartAmt, textvariable=part_amt_string, width=15, anchor=W)
part_amt_string.set("Particle Amount:")

#slider and button for particle amount
particleAmount = DoubleVar()
scalePartAmt = Scale(framePartAmt, variable=particleAmount, from_=1, to=500, orient=HORIZONTAL, length=300)
buttonPartAmtValue = Button(framePartAmt, text="Get Value", command=selPA)
labelPartAmtValue = Label(framePartAmt, text="Value = 250.0")
scalePartAmt.set(250)

#label for funnel height
funnel_height_string = StringVar()
labelTitleFunnelHeight = Label(frameFunHeight, textvariable=funnel_height_string, width=15, anchor=W)
funnel_height_string.set("Hourglass Height:")

#slider and button for funnel height
funnelHeight = DoubleVar()
scaleFunHeight = Scale(frameFunHeight, variable=funnelHeight, from_=0, to=200, orient=HORIZONTAL, length=300)
buttonFunHeightValue = Button(frameFunHeight, text="Get Value", command=selFH)
labelFunHeightValue = Label(frameFunHeight, text="Value = 100.0")
scaleFunHeight.set(100)

#label for funnel radius
funnel_radius_string = StringVar()
labelTitleFunnelRadius = Label(frameFunRadius, textvariable=funnel_radius_string, width=15, anchor=W)
funnel_radius_string.set("Hourglass Radius:")

#slider and button for funnel radius
funnelRadius = DoubleVar()
scaleFunRadius = Scale(frameFunRadius, variable=funnelRadius, from_=1, to=100, orient=HORIZONTAL, length=300)
buttonFunRadiusValue = Button(frameFunRadius, text="Get Value", command=selFR)
labelFunRadiusValue = Label(frameFunRadius, text="Value = 20.0")
scaleFunRadius.set(20)

#insert into framePartSize
labelTitlePartSize.grid(row=0, column=0, sticky=S)
scalePartSize.grid(row=0, column=2)
buttonPartSizeValue.grid(row=0, column=3, sticky=S)
labelPartSizeValue.grid(row=0, column=4, sticky=S)

#insert into framePartMass
labelTitlePartMass.grid(row=0, column=0, sticky=S)
scalePartMass.grid(row=0, column=2)
buttonPartMassValue.grid(row=0, column=3, sticky=S)
labelPartMassValue.grid(row=0, column=4, sticky=S)

#insert into framePartAmt
labelTitlePartAmt.grid(row=0, column=0, sticky=S)
scalePartAmt.grid(row=0, column=2)
buttonPartAmtValue.grid(row=0, column=3, sticky=S)
labelPartAmtValue.grid(row=0, column=4, sticky=S)

#insert into frameFunHeight
labelTitleFunnelHeight.grid(row=0, column=0, sticky=S)
scaleFunHeight.grid(row=0, column=2)
buttonFunHeightValue.grid(row=0, column=3, sticky=S)
labelFunHeightValue.grid(row=0, column=4, sticky=S)

#insert into frameFunRadius
labelTitleFunnelRadius.grid(row=0, column=0, sticky=S)
scaleFunRadius.grid(row=0, column=2)
buttonFunRadiusValue.grid(row=0, column=3, sticky=S)
labelFunRadiusValue.grid(row=0, column=4, sticky=S)

#button to collect all data
buttonAllValues = Button(frameButtons, text="Run Simulation", command=selAllVariables)
buttonAllValues.grid(row=1, column=0, sticky=E)

#begin Loop
window.mainloop()
