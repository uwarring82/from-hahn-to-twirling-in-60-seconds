"""Finite-pulse Bloch model. Run with Python 3, NumPy and Matplotlib."""
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial.hermite import hermgauss

T = 200e-6                 # total free precession, seconds
RABI = 50e3                # nominal resonant Rabi frequency, Hz
AREA = 1.01                # actual / nominal Rabi frequency
JITTER = 100.0             # shot-static detuning rms, Hz
VIS = 0.95                 # independent common contrast factor
N = 2000                   # binary shots per quadrature per protocol
nodes, weights = hermgauss(24)
weights /= np.sqrt(np.pi)

def evolve(v, drive, offset, duration):
    field = np.array([drive, 0, offset])
    norm = np.linalg.norm(field)
    if norm == 0:
        return v
    axis = field / norm
    angle = 2*np.pi*norm*duration
    return (v*np.cos(angle) + np.cross(axis, v)*np.sin(angle)
            + axis*np.dot(axis,v)*(1-np.cos(angle)))

def sequence(offset, mode):
    v = np.array([1., 0., 0.])   # prepared +X; common readout defined in lab frame
    def pulse(v):
        return evolve(v, AREA*RABI, offset, 0.5/RABI)
    def free(v, t):
        return evolve(v, 0, offset, t)
    if mode == 'echo':
        # Closing X returns the toggling frame to the common analysis frame.
        return pulse(free(pulse(free(v,T/2)),T/2))
    if mode == 'X':
        return pulse(free(pulse(v),T))
    return free(v,T)

def predict(offset, mode):
    return VIS*sum(w*sequence(offset+np.sqrt(2)*JITTER*x,mode)
                   for x,w in zip(nodes,weights))

def signals(f):
    echo = predict(f,'echo')
    twirl = (predict(f,'I')+predict(f,'X'))/2
    return echo, twirl

if __name__ == '__main__':
    offsets = np.linspace(0,2500,101)
    results = np.array([signals(f) for f in offsets])
    for idx in [0,25,50,75,100]:
        print(offsets[idx],results[idx,:,:2].round(5))
    # Check the zero-duration-pulse limit at finite rotation angle.
    previous = (RABI, AREA, JITTER, VIS)
    RABI, AREA, JITTER, VIS = 1e12, 1., 0., 1.
    for f in [0,625,1250,1875,2500]:
        e,t = signals(f)
        assert np.allclose([*e[:2],*t[:2]],[1,0,np.cos(2*np.pi*f*T),0],atol=1e-7)
    RABI, AREA, JITTER, VIS = previous
    fig, ax = plt.subplots(figsize=(7.4,3.8),layout='constrained')
    for i,label,color in [(0,'Hahn echo','#175878'),(1,'Channel twirl','#ad452b')]:
        ax.plot(offsets/1000,results[:,i,0],color=color,lw=2.5,label=label)
    ax.axhline(0,color='0.6',lw=0.8)
    ax.axvline(1.25,color='0.6',ls=':')
    ax.set(xlabel='Imposed detuning (kHz)',ylabel='Signed Ramsey X quadrature',ylim=(-1.05,1.05))
    ax.legend(frameon=False)
    fig.savefig('echo_twirl.svg')
