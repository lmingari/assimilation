import pandas as pd
import numpy as np
import xarray as xr
from os.path import join
import sys
from configparser import ConfigParser

###
### Read configuration file
###
config = ConfigParser(inline_comment_prefixes="#")
config.read('config.ini')

####
#### Parameters
####
path_obs        = config.get('DATA','path')
debug           = True

###
### Information screen
###
if debug:
    print("""
    --------------------------
    Compute validation metrics
    --------------------------
    """)

try:
    path = sys.argv[1]
except:
    path = './'

data = []
for percentAss in np.arange(10,100,5):
    ###
    ### Read model data
    ###
    fname_an = "analysis_{:03d}.nc".format(percentAss)
    fname_an = join(path,fname_an) 
    if debug: print("Opening analysis file: {}".format(fname_an))
    ds = xr.open_dataset(fname_an)
    ####
    #### Read obs data
    ####
    fname_obs = "deposit_{:03d}.csv".format(percentAss)
    fname_obs = join(path_obs,fname_obs)
    if debug: print("Opening observation file: {}".format(fname_obs))
    df = pd.read_csv(fname_obs)
    nobs = len(df)
    if debug: print("Number of observations: {}".format(nobs))
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
    ### Compute accuracy metrics
    ###
    for dataset in ["assimilation","validation"]:
        yo = df[df.dataset==dataset]['thickness']
        ye = df[df.dataset==dataset]['error']
        for field in ["forecast","analysis"]:
            ym = df[df.dataset==dataset][field]
            #
            e     = (yo-ym)/ye
            bias  = e.mean()
            mae   = e.abs().mean()
            mse   = (e**2).mean()
            #
            e1    = (yo-ym).abs()
            e2    = yo.abs()+ym.abs()
            smape = (e1[e2>0]/e2[e2>0]).mean()
            #
            hits  = ((ym<3*yo) & (3*ym>yo)).sum()/len(ym)
            #
            data.append({
                'percentAss': percentAss,
                'dataset':    dataset,
                'field':      field,
                'rmse':       np.sqrt(mse),
                'bias':       bias,
                'mae':        mae,
                'smape':      100*smape,
                'hits':       100*hits,
                })

fname_csv = "validation_metrics.csv"
fname_csv = join(path,fname_csv)
if debug: print("Saving output file: {}".format(fname_csv))
df_out = pd.DataFrame(data)
df_out.set_index("percentAss",inplace=True)
df_out.to_csv(fname_csv)
