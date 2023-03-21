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
    -------------------------------
    Compute correlation coefficient
    -------------------------------
    """)

try:
    path = sys.argv[1]
except:
    path = './'

###
### Read model data
###
fname_an = "analysis_100.nc"
fname_an = join(path,fname_an) 
if debug: print("Opening analysis (reference) file: {}".format(fname_an))
ds0 = xr.open_dataset(fname_an)

data = []
for percentAss in np.arange(10,105,5):
    ###
    ### Read model data
    ###
    fname_an = "analysis_{:03d}.nc".format(percentAss)
    fname_an = join(path,fname_an) 
    if debug: print("Opening analysis file: {}".format(fname_an))
    ds = xr.open_dataset(fname_an)
    ###
    ### Compute correlation
    ###
    for field in ["forecast","analysis"]:
        corr = xr.corr(ds['analysis'],ds0[field])
        data.append({
            'percentAss':  percentAss,
            'field':       field,
            'correlation': corr.values
            })

fname_csv = "correlation.csv"
fname_csv = join(path,fname_csv)
if debug: print("Saving output file: {}".format(fname_csv))
df_out = pd.DataFrame(data)
df_out.set_index("percentAss",inplace=True)
df_out.to_csv(fname_csv)
