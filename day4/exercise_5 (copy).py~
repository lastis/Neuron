#!/usr/bin/env python
'''
Simple Hay simulation with one synaptic input
'''
from os.path import join
import numpy as np
import pylab as plt
import neuron
import LFPy
from hay_model.hay_active_declarations import active_declarations
nrn = neuron.h

def return_cell(synaptic_y_pos=900, conductance_type='active', weight=0.001, input_spike_train=np.array([10.])):
    """
    Runs a NEURON simulation and returns an LFPy cell object for a single synaptic input.
    :param synaptic_y_pos: position along the apical dendrite where the synapse is inserted.
    :param conductance_type: Either 'active' or 'passive'. If 'active' all original ion-channels are included,
           if 'passive' they are all removed, yielding a passive cell model.
    :param weight: Strength of synaptic input.
    :param input_spike_train: Numpy array containing synaptic spike times
    :return: cell object where cell.imem gives transmembrane currents, cell.vmem gives membrane potentials.
             See LFPy documentation for more details and examples.
    """
    nrn('forall delete_section()')
    model_path = join('hay_model')
    neuron.load_mechanisms(join(model_path, 'mod'))
    cell_parameters = {
        'morphology': join(model_path, 'cell1.hoc'),
        'v_init': -65,
        'passive': False,
        'nsegs_method': 'lambda_f',
        'lambda_f': 100,
        'timeres_NEURON': 2**-3,  # Should be a power of 2
        'timeres_python': 2**-3,
        'tstartms': -200,
        'tstopms': 200,
        'custom_code': [join(model_path, 'custom_codes.hoc')],
        'custom_fun': [active_declarations],
        'custom_fun_args': [{'conductance_type': conductance_type}],
    }
    cell = LFPy.Cell(**cell_parameters)
    synapse_parameters = {
        'idx': cell.get_closest_idx(x=0., y=synaptic_y_pos, z=0.),
        'e': 0.,
        'syntype': 'ExpSyn',
        'tau': 10.,
        'weight': weight,
        'record_current': True,
    }
    synapse = LFPy.Synapse(cell, **synapse_parameters)
    synapse.set_spike_times(input_spike_train)
    cell.simulate(rec_imem=True, rec_vmem=True)
    return cell

def plot_cell(cell):
    cell_plot_idx = 0
    plt.subplots_adjust(hspace=0.5)  # Adjusts the vertical distance between panels.
    plt.subplot(121, aspect='equal', xticks=[], xlabel='x', ylabel='y [$\mu m$]')
    [plt.plot([cell.xstart[idx], cell.xend[idx]], [cell.ystart[idx], cell.yend[idx]], c='k') for idx in xrange(cell.totnsegs)]
    plt.plot(cell.xmid[cell.synidx], cell.ymid[cell.synidx], 'ro')
    plt.subplot(222, title='Membrane potential', xlabel='Time [ms]', ylabel='mV')
    plt.plot(cell.tvec, cell.vmem[cell_plot_idx, :])
    plt.subplot(224, title='Transmembrane currents', xlabel='Time [ms]', ylabel='nA')
    plt.plot(cell.tvec, cell.imem[cell_plot_idx, :])
    plt.show()

if __name__ == '__main__':
    cell = return_cell()
    plot_cell(cell)