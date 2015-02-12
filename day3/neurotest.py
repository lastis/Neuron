import neuron
import pylab as plt

nrn = neuron.h

soma = nrn.Section("soma")
soma.L = 15	# um
soma.diam = 15	# um
soma.nseg = 1

dend = nrn.Section("dend")
dend.L = 1000	# um
dend.diam = 2	# um
dend.nseg = 100

dend.connect(soma, 1, 0)

for sec in nrn.allsec():
    sec.Ra = 100	# Ohm cm
    sec.cm = 1		# uF / cm2
    sec.insert("hh")
    #sec.g_pas = 1.0 / 30000
    #sec.e_pas = -65

stim = nrn.IClamp(soma(0.5))
stim.delay = 30		# ms
stim.dur = 300		# ms
stim.amp = -0.3		# nA

t = nrn.Vector()
t.record(nrn._ref_t)

v = nrn.Vector()
v.record(dend(1.)._ref_v)

i = nrn.Vector()
i.record(stim._ref_i)

nrn.finitialize()

neuron.run(600)
plt.plot(t,v)
plt.show()
