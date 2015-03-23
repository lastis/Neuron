from __future__ import division
from scipy.stats import norm
from neuron import h, load_mechanisms
from numpy import trapz
cvode = h.CVode()
cvode.active(1)
#cvode.maxstep(0.2)
h.load_file('stdlib.hoc')
import pylab
pylab.interactive(1) 
import matplotlib.cm as cm
celsius = 36.0 # temperature
Epas = -70.6 # reversal potential for leakage current

## SELECT MORPHOLOGY
h("forall delete_section()")
h("sec_counted=0")
h.load_file(1,"Morf_default.hoc") # Default, from Halnes2011
h.load_file(1,"fixnseg.hoc") # Segmentize (technicality)

######################################################################
def test():    
    rall = 113 # axial resistance
    cap = 1.1 # membrane capacitance
    Rm = 45000.0 # membrane resistance
    
    ## INSERT ION CHANNELS:
    for sec in h.allsec():
        sec.insert("pas")
        sec.e_pas = Epas
        sec.g_pas = 1/Rm
        sec.Ra = rall
        sec.cm = cap
        sec.insert("Cad")
        sec.insert("it2")
        sec.insert("hh2")
        sec.ena = 50 # Reversal potential for sodium
        sec.ek = -90 # Reversal potential for potassium

     ##################################################################   
    # Channel densities
    gna = 0 # S/cm2
    gkdr = 0
    gcat = 0

    ###################################################################
    ## INSERT STIMULATION ELECTRODES
    stim = h.IClamp(.5)
    stim.delay = 1000
    stim.dur = 10
    stim.amp = 0 #nA

    ###################################################################
    ## INSERT SYNAPSES    
    syn = h.Exp2Syn(h.dend[99](1)) # Sum of exp's
    syn.tau1 = 0.5 # Rise (ms)
    syn.tau2 = 2 # Decay (ms)
    syn.e = 10 # Reversal # pot.
              
    s = h.NetStim(0.5)
    s.start = 1000  # start for distal synapses
    s.number = 1
    s.noise = 0    
    
    nc = h.NetCon(s,syn,sec = sec)       
    nc.weight[0] = 0

    #################################################################
    # Split the morphology up in a suitable number of segments
    freq = 50
    h.geom_nseg(freq)
    tot = 0
    for sec in h.allsec():
        tot += sec.nseg
    h.distance()
    print "total # of segments (50Hz):", tot      
              
    ##################################################################
    # INITIALIZE
    def initialize():
        global Epas
        h.celsius = celsius
        for sec in h.soma:
            h.distance()    
   
        for sec in h.allsec():
            sec.v = Epas
            sec.e_pas = Epas
    
            sec.insert("pas")
            sec.e_pas = Epas
            sec.g_pas = 1/Rm
            sec.Ra = rall
            sec.cm = cap
            sec.gnabar_hh2 = 0 
            sec.gkbar_hh2 = 0
            sec.gcabar_it2 = gcat
        for sec in h.soma:
            sec.gnabar_hh2 = gna 
            sec.gkbar_hh2 = gkdr
            sec.gcabar_it2 = gcat
                                                                             
        h.finitialize()       
        h.fcurrent()     
        cvode.re_init()
    
    initialize()

    vec ={}
    for var in 't', 'd_sec', 'd_seg', 'diam_sec','gc','diam_seg','stim_curr':
        vec[var] = h.Vector()
        
    for var in 'V_sec', 'V_seg', 'CaConc_sec','CaConc_seg':
        vec[var] = h.List()
    
    def create_lists(vec):        
        for sec in h.allsec():
            vec['d_sec'].append(h.distance(1))
            vec['diam_sec'].append(sec.diam)  
            rec0 = h.Vector()
            rec0.record(sec(0.5)._ref_v)         
            vec['V_sec'].append(rec0)
            rec_Ca = h.Vector()
            rec_Ca.record(sec(0.5)._ref_Cai)
            vec['CaConc_sec'].append(rec_Ca)        
            for seg in sec: 
                vec['d_seg'].append(h.distance(0) + sec.L * seg.x)
                vec['diam_seg'].append(seg.diam)
                vec['gc'].append(seg.gcabar_it2)   
                rec = h.Vector()
                rec.record(seg._ref_v)
                vec['V_seg'].append(rec)
                rec1 = h.Vector()
                rec1.record(seg._ref_Cai)
                vec['CaConc_seg'].append(rec1)                                   
        return vec
    #####################################    	
    create_lists(vec)       
    # run the simulation
    
    vec['t'].record(h._ref_t)
    # vec['current'].record(VC_patch._ref_i)
    vec['stim_curr'].record(stim._ref_i)
    h.load_file("stdrun.hoc")               
    h.tstop = 2500  # Simulation time
    h.t = -500
    h.run()
    return vec            

vec = test()

# ########################################################################
## Plotting propagation of voltage signal 
fig = pylab.figure()

ax1 = fig.add_subplot(4, 1, 1)
ax1.set_title('tittel')
ax1.text(-0.025, 1.025, 'A',horizontalalignment='center',verticalalignment='bottom',fontsize=18, fontweight='demibold',
transform=ax1.transAxes)

ax2 = fig.add_subplot(4, 1, 2, sharex=ax1, sharey=ax1, ylabel='Voltage(mV)')
ax2.text(-0.025, 1.025, 'B',horizontalalignment='center',verticalalignment='bottom',fontsize=18, fontweight='demibold',
transform=ax2.transAxes)

ax3 = fig.add_subplot(4, 1, 3, sharex=ax1, sharey=ax1)
ax3.text(-0.025, 1.025, 'C',horizontalalignment='center',verticalalignment='bottom',fontsize=18, fontweight='demibold',
transform=ax3.transAxes)

ax4 = fig.add_subplot(4, 1, 4, sharex=ax1, sharey=ax1)
ax4.text(-0.025, 1.025, 'D',horizontalalignment='center',verticalalignment='bottom',fontsize=18, fontweight='demibold',
transform=ax4.transAxes)

# 0, 83, 88, 99 are selected points along a single dendritic branch
ax1.plot(vec['t'], vec['V_sec'][0], label = 'At soma') 
ax2.plot(vec['t'], vec['V_sec'][83], label = '%1.1f $\mu$m' %vec['d_sec'][83]) 
ax3.plot(vec['t'], vec['V_sec'][88], label = '%1.1f $\mu$m' % vec['d_sec'][88])
ax4.plot(vec['t'], vec['V_sec'][99], label = '%1.1f $\mu$m' % vec['d_sec'][99]) 
ax1.legend(loc='best',frameon=False, fontsize=13)
ax2.legend(loc='best',frameon=False, fontsize=13)
ax3.legend(loc='best',frameon=False, fontsize=13)
ax4.legend(loc='best',frameon=False, fontsize=13)
pylab.setp([a.set_xlabel('') for a in [ax1,ax2,ax3]], visible=False) 
pylab.setp([a.get_xticklabels() for a in [ax1,ax2,ax3]], visible=False)

