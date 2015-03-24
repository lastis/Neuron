from nest import *
from pprint import pprint
import nest.voltage_trace as voltage_trace

t_sim = 1000


models = Models("all")
#neuron = Create("iaf_psc_delta_canon")
neuron = Create("iaf_neuron")
current = Create("dc_generator")
voltmeter = Create("voltmeter")

SetStatus(current,"amplitude",500.0)
#SetStatus(voltmeter,{"interval":10.0,"withgid":True})

Connect(voltmeter,neuron)
Connect(current,neuron)


Simulate(t_sim)
voltage_trace.from_device(voltmeter)
voltage_trace.show()

"""
stats = GetStatus()
pprint(stats)
"""


