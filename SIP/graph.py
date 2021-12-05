import matplotlib.pyplot as plt

import pygimli as pg
import numpy as np
#### make definition for plotting the 2D interpolation result
from matplotlib.colors import LogNorm

import matplotlib.pyplot as plt
import re


from scipy.interpolate import interp2d, Rbf
from mpl_toolkits import axes_grid1

from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.axes_grid1 import make_axes_locatable
### https://stackoverflow.com/questions/18195758/set-matplotlib-colorbar-size-to-match-graph
    

def showAmplitudeSpectrum(*args, **kwargs):
    pg.deprecated('drawAmplitudeSpectrum')
    return drawAmplitudeSpectrum(*args, **kwargs)


def showPhaseSpectrum(*args, **kwargs):
    pg.deprecated('drawPhaseSpectrum')
    return drawPhaseSpectrum(*args, **kwargs)


def drawAmplitudeSpectrum(ax, freq, amp, ylabel=r'$\rho$ ($\Omega$m)',
                          grid=True, marker='+', ylog=True, **kwargs):
    """Show amplitude spectrum (resistivity as a function of f)."""
    if 'label' not in kwargs:
        kwargs['label'] = 'obs'
        
    gci = ax.semilogx(freq, amp, marker=marker, **kwargs)
    if ylog is None:
        ylog = (min(amp) > 0)
    if ylog:
        ax.set_yscale('log')
    #ax.set_ylim(min(amp) * .99, max(amp * 1.01))
    ax.set_xlabel('f (Hz)')
    ax.set_ylabel(ylabel)
    ax.grid(grid)
    ax.legend()
    return gci

def drawPhaseSpectrum(ax, freq, phi, ylabel=r'$-\phi$ (mrad)',
                      grid=True, marker='+', ylog=False, **kwargs):
    """Show phase spectrum (-phi as a function of f)."""
    if 'label' not in kwargs:
        kwargs['label'] = 'obs'

    gci = ax.semilogx(freq, phi, marker=marker, **kwargs)
    if ylog:
        ax.set_yscale('log')
    ax.set_xlabel('f (Hz)')
    ax.set_ylabel(ylabel)
    ax.grid(grid)
    ax.legend()
    return gci


def showSpectrum(freq, amp, phi, nrows=2, ylog=None, axs=None, **kwargs):
    """Show amplitude and phase spectra in two subplots."""
    if axs is None:
        fig, axs = plt.subplots(nrows=nrows, sharex=(nrows == 2))
    else:
        fig = axs[0].figure
    drawAmplitudeSpectrum(axs[0], freq, amp, ylog=ylog, **kwargs)
    drawPhaseSpectrum(axs[1], freq, phi, ylog=ylog, **kwargs)
    return fig, axs


def plotSpectrum(ax, freq, vals, ylabel=r'$-\phi$ (mrad)',
                 grid=True, marker='+', ylog=True, **kwargs):
    """Plot some spectrum (redundant).
    DEPRECATED
    """
    pg.deprecated('drawSpectrum')
    if 'label' not in kwargs:
        kwargs['label'] = 'obs'
    ax.loglog(freq, vals, marker=marker, **kwargs)
    if ylog:
        ax.set_yscale('log')
    ax.set_xlabel('f (Hz)')
    ax.set_ylabel(ylabel)
    ax.grid(grid)


""""""

#### Make definition for 2D interpolation data
def interpolate_2D(data1, data2, data3, val_limit):
    
    x = np.array(data1)
    y = np.array(data2)
    a = np.array(data3)
    
    xi, yi = np.mgrid[x.min():x.max():500j, y.min():y.max():500j]
       
    
    rbf = Rbf(x, y, a)
    ai = rbf(xi, yi)
    
    #### modify the result from interpolation --> result can be <0 
    used_data = np.zeros(ai.shape)
    used_data[ai < val_limit] = val_limit
    used_data[ai > val_limit] = ai[ai > val_limit]
    
    return used_data


def plotting_2D(interpolate_data, data, min_val, max_val, norm, title, getcmap):
    
    fig = plt.figure(figsize = (9, 5))
    ax = fig.add_subplot(111)
    
    
    im = ax.imshow(interpolate_data.T, origin='lower',
                   extent=[data.X.min(), data.X.max(), data.Z.min(), data.Z.max()],
                   interpolation = 'nearest',
                   norm = norm,
                   vmin = min_val, vmax = max_val,           
                   cmap = plt.cm.get_cmap(getcmap))
    
    ax.set_xlabel('X [m]', fontsize = 16)
    ax.set_ylabel('Z [m]', fontsize = 16)
#     ax.set_title(title, fontsize = 16)
    
    plt.rc('font', size=14)   # tick font size   


    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="2%", pad=0.07)
    plt.colorbar(im, cax = cax, label=title)
    
    #plt.savefig(output_path+title+'.png') 
    plt.show()    
    
    return


""""""