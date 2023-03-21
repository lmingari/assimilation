import pandas as pd
import numpy as np
from metrics import get_affinity
from sklearn.cluster import SpectralClustering
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
n_clusters      = config.getint(block,'n_clusters')
thickness_min   = config.getfloat(block,'thickness_min')
debug           = True

###
### Information screen
###
if debug:
    print("""
    --------------------------------------------------
    Apply spectral clustering to an observation dataset
    --------------------------------------------------
    Input parameters:
    number of clusters = {n_clusters}
    minimum thickness = {thickness_min} cm
    """.format(n_clusters = n_clusters,
               thickness_min = thickness_min,
               )
          )

# i. Assimilation dataset:
# ------------------------
# Original dataset. Reported by Van Eaton et al. 2016
# https://doi.org/10.1002/2016GL068076
#
# ii. Validation dataset:
# -----------------------
# Reckziegel (personal communication)
fname_in = {"validation":   'grl54177.csv',
            "assimilation": 'reckziegel.csv'}

### Read observations
df_list=[]
for key in fname_in:
    if debug: print("Opening observation file: {}".format(fname_in[key]))
    df = pd.read_csv(fname_in[key], index_col=0)
    df["dataset"] = key
    df_list.append(df)
df = pd.concat(df_list)
df['thickness'] = (df.thickness_max + df.thickness_min)*0.5

#Remove ambiguous data
df.drop(['Cz.18','CAL002','Cz.n.a.2'],inplace=True)

#Remove repeated data
df.drop(['C22'],inplace=True)

#Compute similarity matrix
A = get_affinity(df, thickness_min)

#Clustering
model = SpectralClustering(
        n_clusters=n_clusters,
        affinity = 'precomputed',
        )
labels = model.fit_predict(A)
df['cluster'] = labels
df.sort_values('cluster',inplace=True)
df.set_index('cluster', inplace=True)

#Output dataset
if debug: print("Saving output file: {}".format(fname_clusters))
column_list = ["latitude","longitude","thickness"]
df.to_csv(fname_clusters,columns=column_list)

