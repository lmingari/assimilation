import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from os.path import join
from configparser import ConfigParser

###
### Read configuration file
###
config = ConfigParser(inline_comment_prefixes="#")
config.read('config.ini')

###
### Parameters
###
block           = "GNC"
path            = config.get(block,'path')
fname_src       = config.get(block,'fname_src')
density         = config.getfloat(block,'bulk_density')
fname_plt       = "figures/source.png"
debug           = True

###
### Information screen
###
if debug:
    print(f"""
    ----------------------------------
    Plot emission source term profiles
    ----------------------------------
    Input parameters:
    Bulk density = {density} kg/m3
    """)

fmt = "%d %B %Y at %H UTC"
plot_conf = {
        'path': path,
        'time': datetime(2015,4,22).strftime(fmt),
        }
###
### Plot emission source profiles
###
fig, ax = plt.subplots(figsize=(10,6))

path      = plot_conf['path']
time      = plot_conf['time']
###
### Open ensemble of emission source terms
###
if debug: print(f"Opening emisison source file: {fname_src}")
ds = xr.open_dataset(fname_src)
###
### Open factor weights
###
fname_w = join(path,f"factors_w.nc")
if debug: print(f"Opening weight factors file: {fname_w}")
da = xr.open_dataarray(fname_w)
ds['w'] = da 
#
X = ds.time.values / 3600.0 # time in h
Z = ds.lev.values  / 1000.0 # hight asl in km
DT = (X[1]-X[0])*3600.      # time interval in sec
#
C = ds.src.dot(ds.w).values / 1000.0
M = ds.mfr.dot(ds.w).values
#
im = ax.pcolormesh(X,Z,C.T,
        shading = 'gouraud',
        cmap    = 'YlOrRd')
cbar = fig.colorbar(im,
        orientation = "horizontal", 
        shrink      = .75,
        label       = r'Linear source emission strength ($\times 10^3$) [$kg~s^{-1}~m^{-1}$]',
        ax=ax)
ax2 = ax.twinx()
l2, = ax2.plot(X,1E-6*M,
        label     = "Emission rate", 
        color     = "blue",
        linestyle = "dashdot")
ax3 = ax.twinx()
l3, = ax3.plot(X,DT*1E-9*M.cumsum()/density,
        label     = "Cumulative Erupted Volume",
        color     = "black",
        linestyle = "solid")

ax.text(19.0,15.0,
        "1st eruptive\nphase",
        horizontalalignment='center',
        bbox={'facecolor': 'white', 'alpha': 0.5},
       )
ax.text(26.0,12,
        "2nd eruptive\nphase",
        horizontalalignment='center',
        bbox={'facecolor': 'white', 'alpha': 0.5},
       )

###
### Configure plots
###
ax.set(
    ylabel = 'Altitude [km asl]',
    xlabel = f'Simulation time [hours since {time}]',
    xlim   = [15,40],
    ylim   = [0,22],
    )
ax2.set(
    ylabel = r'Emission rate ($\times 10^6$) [kg/s]',
    )
ax2.spines['left'].set_position(('outward', 50))
ax2.yaxis.set_label_position("left")
ax2.yaxis.set_ticks_position('left')
ax3.set(
    ylabel = r'Cumulative Erupted Volume [$km^3$]',
    ylim   = [0,0.32],
    )

plt.legend( handles=[l2,l3] )

#erupted = DT*1E-9*M.cumsum()/density
#print("Total volume erupted:")
#print(erupted)

ds.close()

if debug: print(f"Saving plot: {fname_plt}")
fig.savefig(fname_plt,
            dpi=200,
            bbox_inches='tight')
