def calculateWeight():
    global particleSize
    global particleMass
    global funnelSize
    global funnelRadius
    partSize = particleSize.get()
    partMass = particleMass.get()
    funSize = funnelSize.get()
    funRadius = funnelRadius.get()

    print(partSize)
    print(partMass)
    print(funSize)
    print(funRadius)

from tkinter import *

root = Tk()

root.title("Hourglass Simulation")

label_1 = Label(root, text="Particle Size")
label_2 = Label(root, text="Particle Mass")
label_3 = Label(root, text="Height of Funnel")
label_4 = Label(root, text="Radius of Funnel")

particleSize = Entry(root)
particleMass = Entry(root)
funnelSize = Entry(root)
funnelRadius = Entry(root)

label_1.grid(row=0, sticky=E)
label_2.grid(row=1, sticky=E)
label_3.grid(row=2, sticky=E)
label_4.grid(row=3, sticky=E)

particleSize.grid(row=0, column=1)
particleMass.grid(row=1, column=1)
funnelSize.grid(row=2, column=1)
funnelRadius.grid(row=3, column=1)

calculateButton = Button(root, text="calculate", command=calculateWeight)
calculateButton.grid(columnspan=2)

root.mainloop()
