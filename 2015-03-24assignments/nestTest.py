import nest
import matplotlib.pyplot as plt
import numpy as np



def buildNetwork(I_e, t_sim):
    nest.ResetKernel()
    nest.SetDefaults("iaf_psc_delta",{"I_e" : I_e})
    neuron = nest.Create("iaf_psc_delta")
    voltmeter = nest.Create("voltmeter")
    detector = nest.Create("spike_detector")

    nest.Connect(voltmeter,neuron)
    nest.Connect(neuron,detector)

    nest.Simulate(t_sim)

    return voltmeter, detector




# 1.2.3 #1
# voltmeter, detector = buildNetwork(500.,50.)
# V = nest.GetStatus(voltmeter,'events')[0]['V_m']
# t = nest.GetStatus(voltmeter,'events')[0]['times']
# s = nest.GetStatus(detector,'events')[0]['times']

# plt.plot(t,V)
# plt.plot(s,-54*np.ones(len(s)), 'o')
# plt.show()

# N = 101
# IeVec = np.linspace(400,450,N)

# spikes = np.zeros(len(IeVec))
# for i in xrange(N):
#     voltmeter, detector = buildNetwork(IeVec[i],50.)
#     V = nest.GetStatus(voltmeter,'events')[0]['V_m']
#     t = nest.GetStatus(voltmeter,'events')[0]['times']
#     s = nest.GetStatus(detector,'events')[0]['times']
#     spikes[i] = len(s)

# plt.plot(IeVec,spikes)
# plt.show()


# 1.2.3 #2
# N = 101
# IeVec = np.linspace(300,400,N)
# spikes = np.zeros(len(IeVec))
# for i in xrange(N):
#     voltmeter, detector = buildNetwork(IeVec[i],1000.)
#     V = nest.GetStatus(voltmeter,'events')[0]['V_m']
#     t = nest.GetStatus(voltmeter,'events')[0]['times']
#     s = nest.GetStatus(detector,'events')[0]['times']
#     spikes[i] = len(s)

# plt.plot(IeVec,spikes)
# plt.show()

# def buildNetwork2(I_e, t_sim, myseed):
#     nest.ResetKernel()
#     nest.SetKernelStatus({'grng_seed': myseed, 'rng_seeds':[myseed + 1]})
#     nest.SetDefaults("iaf_psc_delta",{"I_e" : I_e})
#     neuron = nest.Create("iaf_psc_delta")
#     voltmeter = nest.Create("voltmeter")
#     detector = nest.Create("spike_detector")
#     noise = nest.Create("noise_generator", params={"mean": 0.0, "std" : 30.})

#     nest.Connect(voltmeter,neuron)
#     nest.Connect(neuron,detector)
#     nest.Connect(noise,neuron)

#     nest.Simulate(t_sim)

#     return voltmeter, detector

# voltmeter, detector = buildNetwork2(365.,1000.,0)
# V = nest.GetStatus(voltmeter,'events')[0]['V_m']
# t = nest.GetStatus(voltmeter,'events')[0]['times']
# s = nest.GetStatus(detector,'events')[0]['times']

# plt.plot(t,V)
# plt.plot(s,-54*np.ones(len(s)), 'o')
# plt.show()

# Validation
# def buildNetwork2(I_e, t_sim, myseed):
#     nest.ResetKernel()
#     nest.SetKernelStatus({'grng_seed': myseed, 'rng_seeds':[myseed + 1]})
#     nest.SetDefaults("iaf_psc_delta",{"I_e" : 0.0})
#     neuron = nest.Create("iaf_psc_delta")
#     voltmeter = nest.Create("voltmeter")
#     detector = nest.Create("spike_detector")
#     noise = nest.Create("noise_generator", params={"mean": I_e, "std" : 0.})

#     nest.Connect(voltmeter,neuron)
#     nest.Connect(neuron,detector)
#     nest.Connect(noise,neuron)

#     nest.Simulate(t_sim)

#     return voltmeter, detector

# voltmeter, detector = buildNetwork2(385.,100.,0)
# V1 = nest.GetStatus(voltmeter,'events')[0]['V_m']
# t1 = nest.GetStatus(voltmeter,'events')[0]['times']
# s1 = nest.GetStatus(detector,'events')[0]['times']


# voltmeter, detector = buildNetwork(385.,100.)
# V2 = nest.GetStatus(voltmeter,'events')[0]['V_m']
# t2 = nest.GetStatus(voltmeter,'events')[0]['times']
# s2 = nest.GetStatus(detector,'events')[0]['times']

# plt.plot(t1,V1,label="1")
# plt.plot(t2,V2,label="2")
# plt.legend()
# plt.show()

# deltaT = s2[0] - s1[0]

# plt.plot(t1,V1,label="1")
# plt.plot(t2-deltaT,V2,label="2")
# plt.legend()
# plt.show()

# 1.3.4 exploration
def buildNetwork3(I_e, t_sim, myseed, std):
    nest.ResetKernel()
    nest.SetKernelStatus({'grng_seed': myseed, 'rng_seeds':[myseed + 1]})
    nest.SetDefaults("iaf_psc_delta",{"I_e" : I_e})
    neuron = nest.Create("iaf_psc_delta")
    voltmeter = nest.Create("voltmeter")
    detector = nest.Create("spike_detector")
    noise = nest.Create("noise_generator", params={"mean": 0.,  "std" : std})

    nest.Connect(voltmeter,neuron)
    nest.Connect(neuron,detector)
    nest.Connect(noise,neuron)

    nest.Simulate(t_sim)

    return voltmeter, detector

Ie = 378.

# # 1.3.4 exploration #1
# voltmeter, detector = buildNetwork3(Ie,100., 0, 10.)
# V1 = nest.GetStatus(voltmeter,'events')[0]['V_m']
# t1 = nest.GetStatus(voltmeter,'events')[0]['times']
# s1 = nest.GetStatus(detector,'events')[0]['times']

# voltmeter, detector = buildNetwork3(Ie,100., 2, 20.)
# V2 = nest.GetStatus(voltmeter,'events')[0]['V_m']
# t2 = nest.GetStatus(voltmeter,'events')[0]['times']
# s2 = nest.GetStatus(detector,'events')[0]['times']

# voltmeter, detector = buildNetwork3(Ie,100., 4, 30.)
# V3 = nest.GetStatus(voltmeter,'events')[0]['V_m']
# t3 = nest.GetStatus(voltmeter,'events')[0]['times']
# s3 = nest.GetStatus(detector,'events')[0]['times']

# plt.plot(t1,V1,label="1")
# plt.plot(t2,V2,label="2")
# plt.plot(t3,V3,label="3")
# plt.legend()
# plt.show()



# 1.3.4 exploration #2
Ie = 378.
bins = 100
voltmeter, detector = buildNetwork3(Ie, 100*1000., 0, 10.)
V1 = nest.GetStatus(voltmeter,'events')[0]['V_m']
t1 = nest.GetStatus(voltmeter,'events')[0]['times']
s1 = nest.GetStatus(detector,'events')[0]['times']
hist1, binVec = np.histogram(V1,bins)
plt.plot(binVec[:-1],hist1, label="1")

voltmeter, detector = buildNetwork3(Ie, 100*1000., 0, 20.)
V2 = nest.GetStatus(voltmeter,'events')[0]['V_m']
t2 = nest.GetStatus(voltmeter,'events')[0]['times']
s2 = nest.GetStatus(detector,'events')[0]['times']
hist2, binVec = np.histogram(V2,bins)
plt.plot(binVec[:-1],hist2, label="2")

voltmeter, detector = buildNetwork3(Ie, 100*1000., 0, 30.)
V3 = nest.GetStatus(voltmeter,'events')[0]['V_m']
t3 = nest.GetStatus(voltmeter,'events')[0]['times']
s3 = nest.GetStatus(detector,'events')[0]['times']
hist3, binVec = np.histogram(V3,bins)
plt.plot(binVec[:-1],hist3, label="3")

plt.legend()

plt.show()








