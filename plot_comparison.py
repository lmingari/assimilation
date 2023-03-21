import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
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
path_obs        = config.get('DATA','path')
fname_plt       = "figures/comparison.png"
percentAss      = 60
xmin,xmax       = 1E-4,1E2
debug           = True

rows = [
        {'label':"First guess",
         'path': 'GNC',
         'field': 'forecast',
         },
        {'label':"GNC",
         'path': 'GNC',
         'field': 'analysis',
         },
        {'label':"EnKF",
         'path': 'ENKF',
         'field': 'analysis',
         },
        {'label':"GIG",
         'path': 'GIG/001',
         'field': 'analysis',
         },
        ]

datasets = ["assimilation","validation"]
###
### Plot model vs observations
###
fig, axs = plt.subplots(
        nrows=len(rows),
        ncols=len(datasets),
        sharex='col',
        sharey=True,
        figsize=(10,15)
        )

####
#### Read obs data
####
fname_obs = "deposit_{:03d}.csv".format(percentAss)
fname_obs = join(path_obs,fname_obs)
if debug: print("Opening observation file: {}".format(fname_obs))
df = pd.read_csv(fname_obs)
nobs = len(df)
if debug: print("Number of observations: {}".format(nobs))

for i,item in enumerate(rows):
    path  = item['path']
    field = item['field']
    label = item['label']
    ###
    ### Read model data
    ###
    fname_an = "analysis_{:03d}.nc".format(percentAss)
    fname_an = join(path,fname_an) 
    if debug: print("Opening analysis file: {}".format(fname_an))
    ds = xr.open_dataset(fname_an)
    ###
    ### Interpolation to observation sites
    ###
    if debug: print("Performing interpolations")
    lat_obs = xr.DataArray(df['latitude'], dims='loc')
    lon_obs = xr.DataArray(df['longitude'],dims='loc')
    y       = ds.interp(lat=lat_obs,lon=lon_obs)
    df['forecast'] = y.forecast
    df['analysis'] = y.analysis
    ###
    ### Plot 
    ###
    for j,dataset in enumerate(datasets):
        yo = df[df.dataset==dataset]['thickness']
        ye = df[df.dataset==dataset]['error']
        y  = df[df.dataset==dataset][field]
        #
        axs[i,j].plot(y,yo,
                      marker = 'o',
                      ls     = 'none',
                      color  = 'tab:red',
                      alpha  = 0.7,
                      label  = label,
                      )
        axs[i,j].plot([xmin,xmax],[xmin,xmax],'k-',        label="Ideal")
        axs[i,j].plot([xmin,xmax],[10*xmin,10*xmax],'k--', label="1:10 ratio")
        axs[i,j].plot([xmin,xmax],[0.1*xmin,0.1*xmax],'k--')

for ax in axs.flat:
    ax.legend()
    ax.grid()
    ax.set(ylabel = 'Deposit thickness - Observation [cm]',
           xlabel = 'Deposit thickness - Analysis/Forecast [cm]',
           xscale = 'log',
           yscale = 'log',
           xlim = (xmin,xmax),
           ylim = (xmin,xmax),
           )
    ax.label_outer()

axs[0,0].set_title("Assimilation dataset")
axs[0,1].set_title("Validation dataset")
fig.tight_layout()
fig.savefig(fname_plt,
            dpi=200,
            bbox_inches='tight')
