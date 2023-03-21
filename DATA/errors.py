import numpy as np
import pandas as pd
from metrics import get_affinity
from configparser import ConfigParser

###
### Read configuration file
###
config = ConfigParser(inline_comment_prefixes="#")
config.read('../config.ini')

###
### Parameters
###
block           = 'DATA'
fname_clusters  = config.get(block,'fname_clusters')
thickness_min   = config.getfloat(block,'thickness_min')
relative_error  = config.getfloat(block,'relative_error')
debug           = True

###
### Information screen
###
if debug:
    print("""
    --------------------------------------------------
    Add errors to an observation dataset with clusters
    --------------------------------------------------
    Input parameters:
    minimum thickness = {thickness_min} cm
    default relative error = {relative_error} %
    """.format(thickness_min = thickness_min,
               relative_error = 100*relative_error,
               )
          )

### Open dataset
if debug: print("Opening observation file: {}".format(fname_clusters))
df = pd.read_csv(fname_clusters)
nobs = len(df)

### Compute errors
if debug: print("Computing errors")
minimum_error = thickness_min * relative_error
df['true']  = df.groupby("cluster")["thickness"].transform('mean')
df['error'] = df.groupby("cluster")["thickness"].transform('std')
df['error'].where(df.error>0.0,relative_error*df.true, inplace=True)
df['error'].where(df.error>minimum_error,minimum_error, inplace=True)
df['error_r'] = df.error/df.true

### Define validation/assimilation datasets
A = get_affinity(df, thickness_min)
for percentAss in np.arange(5,105,5):
    if percentAss<100:
        df['dataset'] = 'validation'
        nobsAss = int(percentAss*0.01*nobs)
        mask = ~np.diag(np.full(nobs,True))
        for iobs in range(nobsAss):
            maxAff = np.amax(A, axis=1, where=mask, initial=-1)
            maxAff[maxAff<0] = 1.0
            imin = np.argmin(maxAff)
            mask[imin,:] = False
            mask[:,imin] = False
            df.iloc[imin,df.columns.get_loc('dataset')] = 'assimilation'
    else:
        df['dataset'] = 'assimilation'
    fname_obs = "deposit_{:03d}.csv".format(percentAss)
    ###
    ### Output table
    ###
    if debug: print("Saving output file: {}".format(fname_obs))
    df.to_csv(fname_obs,
              columns=["latitude",
                       "longitude",
                       "thickness",
                       "error",
                       "error_r",
                       "dataset",
                       "cluster",
                       ],
              index=False)
