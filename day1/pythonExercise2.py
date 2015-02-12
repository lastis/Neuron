from numpy import *
from pylab import *
from numpy import random


V0 = 0
Rm = 0.04
Tm = 10
I = 400
theta = 15
T = 1000
h = 0.1
N = float(T)/h

V = zeros(N)
t = zeros(N)

def simulate(V,t,I):
    V[0] = V0
    n = 0
    Spikes = 0
    while n < N-1:
        t[n+1] = n*h + h
        noise = random.normal(0,50)
        I = I + noise
        V[n+1] = V[n] + h/Tm*(-V[n]+Rm*I)
        if V[n+1] >= theta:
            V[n+1] = 0
            Spikes += 1
        I = I - noise
        n +=1 
    return V,t,Spikes

rSpikes1 = zeros(1000/10)
n = 0

for I in arange(0,1000,10):
    rV,rt,rSpikes1[n] = simulate(V,t,I)
    n += 1

I = arange(0,1000,10)
plot(I,rSpikes1)
show()




