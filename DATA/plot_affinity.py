import numpy as np
import pandas as pd
from metrics import get_affinity
import matplotlib.pyplot as plt
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
fname_out       = '../figures/affinity_matrix.png'
fname_clusters  = config.get(block,'fname_clusters')
thickness_min   = config.getfloat(block,'thickness_min')
debug           = True

###
### Information screen
###
if debug:
    print("""
    -----------------------------------------------
    Plot affinity matrix from a clusterised dataset
    -----------------------------------------------
    Input parameters:
    minimum thickness = {thickness_min} cm
    """.format(thickness_min = thickness_min,
               )
          )

###
### Open dataset
###
if debug: print("Opening observation file: {}".format(fname_clusters))
df = pd.read_csv(fname_clusters)

###
### Compute similarity matrix
###
A = get_affinity(df, thickness_min)

###
### Plot matrix
###
fig,ax=plt.subplots()
im = ax.imshow(A)

size_cum=0
for size in df.groupby('cluster').size():
    xmin,xmax = size_cum-0.5,size_cum+size-0.5
    ax.plot([xmin,xmax],[xmin,xmin],'r-')
    ax.plot([xmin,xmax],[xmax,xmax],'r-')
    ax.plot([xmin,xmin],[xmin,xmax],'r-')
    ax.plot([xmax,xmax],[xmin,xmax],'r-')
    size_cum += size

cbar = fig.colorbar(im)
cbar.set_label("Affinity")

###
### Output plot
###
if debug: print("Saving output file: {}".format(fname_out))
plt.savefig(fname_out,dpi=200,bbox_inches='tight')
