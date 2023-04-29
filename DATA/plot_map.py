import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as crs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
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
fname_out       = '../figures/map_clustering.png'
fname_clusters  = config.get(block,'fname_clusters')
debug           = True

###
### Information screen
###
if debug:
    print("""
    -------------------------------
    Plot observation sites on a map
    -------------------------------
    """)

###
### Open dataset
###
if debug: print("Opening observation file: {}".format(fname_clusters))
df = pd.read_csv(fname_clusters)

### Plot map
fig = plt.figure()
ax  = fig.add_subplot(1,1,1, projection=crs.PlateCarree())

countries = cfeature.NaturalEarthFeature(scale='10m',
                                         category='cultural',
                                         name='admin_0_boundary_lines_land',
                                         facecolor='none')
ax.add_feature(cfeature.LAND, color="lightgrey", alpha=0.8)
ax.add_feature(countries,linewidth=0.5)


s = ax.scatter(x          = df.longitude,
               y          = df.latitude,
               c          = df.cluster,
               s          = 15,
               cmap       = 'Paired',
               edgecolors = 'k',
               linewidths = 0.2,
               alpha      = 0.8,
               transform  = crs.PlateCarree())

gl = ax.gridlines(crs=crs.PlateCarree(),
                  draw_labels = True,
                  linewidth   = 0.5, 
                  color       = 'gray', 
                  alpha       = 0.5, 
                  linestyle   = '--')
gl.top_labels   = False
gl.right_labels = False
gl.ylabel_style = {'rotation': 90}

legend = ax.legend(*s.legend_elements(),
                   loc   = "upper right", 
                   ncol  = 3,
                   title = "Clusters")

###
### Output plot
###
if debug: print("Saving output file: {}".format(fname_out))
plt.savefig(fname_out,dpi=200,bbox_inches='tight')
