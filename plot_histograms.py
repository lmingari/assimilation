import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
from scipy.special import gamma
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
block           = 'DEFAULT'
path_obs        = config.get('DATA','path')
fname_obs       = config.get(block,'fname_obs')
fname_ens       = config.get(block,'fname_ens')
bulk_density    = config.getfloat(block,'bulk_density')
fname_plt       = "figures/histograms.png"
debug           = True

###
### Information screen
###
if debug:
    print(f"""
    --------------------------------------
    Plot histograms for the prior ensemble
    --------------------------------------
    Input parameters:
    bulk density = {bulk_density} kg/m3
    """)

###
### Read prior ensemble
###
if debug: print(f"Opening prior ensemble file: {fname_ens}")
ds = xr.open_dataset(fname_ens)
#Convert mass loading (kg/m2) to thickness (cm)
#using deposit bulk density (kg/m3)
fu = 100.0/bulk_density
x = fu*ds.isel(time=-1)['tephra_grn_load']

###
### Read observation locations
###
fname = join(path_obs,fname_obs)
if debug: print(f"Opening observation file: {fname}")
df = pd.read_csv(fname)
indexes_loc = [164,165,108,86,
               198,199,19,203,
               47,68,58,46,
               66,85,84,195,
               ]               
df = df.iloc[indexes_loc]

###
### Perform interpolations
###
if debug: print("Performing interpolations")
lat_obs = xr.DataArray(df['latitude'], dims='loc')
lon_obs = xr.DataArray(df['longitude'],dims='loc')
y = x.interp(lat=lat_obs,lon=lon_obs)

###
### Plot histograms
###
nrows, ncols = 4,4
fig, axs = plt.subplots(
        nrows=nrows,
        ncols=ncols,
        figsize=(14,12)
        )

for i,ax in enumerate(axs.flat):
    lat   = y.isel(loc=i).lat.item()
    lon   = y.isel(loc=i).lon.item()
    y_var = y.isel(loc=i).var().item()
    y_m   = y.isel(loc=i).mean().item()
    #
    # type 2 relative forecast error variance
    #
    p2 = y_var/(y_var+y_m**2)
    p1_inv = 1./p2-1
    #
    # Generate histogram
    #
    n,bins,_ = ax.hist(
            y.isel(loc=i),
            bins=20,
            density=True)
    if i%ncols==0:
        ax.set(ylabel = 'Probability density')
    if i//ncols == nrows - 1:
        ax.set(xlabel = 'Deposit thickness [cm]')

    iid = chr(i+97) 
    ax.text(0.95,0.95,
            f"({iid})\nlat={lat:.2f}\nlon={lon:.2f}",
        horizontalalignment='right',
        verticalalignment='top',
        fontsize = 12,
        transform=ax.transAxes)
    #
    # Plot Gamma PDF
    #
    x_gamma = np.linspace(0.25*bins[1],bins[-1],num=100)
    y_gamma = x_gamma**(p1_inv-1) * np.exp(-p1_inv/y_m*x_gamma)
    y_gamma *= 1.0/(gamma(p1_inv)*(y_m/p1_inv)**p1_inv)
    
    ax.plot(x_gamma,y_gamma,lw=2)
    ax.ticklabel_format(axis="y", style="sci", scilimits=(0,0), useMathText=True)
#    ax.tick_params(axis='y', labelrotation = 90)

fig.tight_layout()

###
### Save plot
###
if debug: print(f"Saving plot: {fname_plt}")
fig.savefig(fname_plt,
            dpi=200,
            bbox_inches='tight')
