from math import *
from visual import *
from visual.graph import *

gd1 = gdisplay(x=1, y=0, title='W(t) v.s. t', xtitle='t', ytitle='W(t)',
               ymin=0, ymax=7, xmax=1)
fot = gcurve(gdisplay=gd1, color=color.yellow)


massup=0.5
massdown=0.0
masst=0.01
g=9.8
h=0.1
vf=sqrt(2.0*g*h)
pf=masst*vf
tf=vf/g
dt=0.01
ttot=massup/masst*0.01+tf
F=massup*g
t=0
impt=0.01
fp=0.0
print massup/masst,tf
while t <= ttot+0.1:
    massup = massup-masst
    if t>= tf:
        fp=pf
        massdown=massdown+masst
        if t > massup/masst:
            massup=0.0
    if t >= ttot:
        fp=0
        massdown=0.5
    F=(massup+massdown)*g+fp/impt
    print F,fp/impt
    fot.plot(pos=(t,F))
    t=t+dt
    
