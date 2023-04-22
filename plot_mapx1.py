import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
import cartopy.crs as crs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
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
fname_out       = 'figures/maps_enkf.png'
fname_obs       = 'DATA/deposit_060.csv'
levels          = config.get(block,'levels')
plot_obs        = True
debug           = True

###
### Information screen
###
if debug:
    print("""
    -------------------------------
    Plot analysis contours on a map
    -------------------------------
    """)

conf = { 
     'label': "EnKF analysis ensemble mean",
     'fname': "ENKF/analysis_060_uncorrected.nc",
     'field': 'analysis',
     }

###
### Plot deposit contours
###
fig = plt.figure(figsize=(9,9))
ax  = fig.add_subplot( 1,1,1, projection=crs.PlateCarree())

levels = [0] + [float(item) for item in levels.split()]
cmap   = plt.cm.RdYlBu_r
norm   = BoundaryNorm(levels,cmap.N)

field = conf['field']
label = conf['label']
fname = conf['fname']
if debug: print("Opening analysis file: {}".format(fname))
ds = xr.open_dataset(fname)

fc = ax.contourf(ds.lon,ds.lat,10.0*ds[field],
                 levels = levels,
                 norm = norm,
                 cmap = cmap,
                 extend='max',
                 transform = crs.PlateCarree()
                 )
ax.set_title(label)

# Draw the colorbar
cbar=fig.colorbar(
        fc, 
        ticks       = levels,
        shrink      = 0.8,
        pad         = 0.05,
        orientation = 'horizontal',
        label       = 'Deposit thickness in mm',
        )

BORDERS = cfeature.NaturalEarthFeature(
        scale='10m',
        category='cultural',
        name='admin_0_boundary_lines_land',
        edgecolor='gray',
        facecolor='none')

LAND = cfeature.NaturalEarthFeature(
        'physical', 'land', '10m',
        edgecolor='none',
        facecolor='lightgrey',
        alpha = 0.8)

ax.add_feature(BORDERS, linewidth=0.4)
ax.add_feature(LAND,zorder=0)

gl = ax.gridlines(crs=crs.PlateCarree(),
                  draw_labels = True,
                  linewidth   = 0.5, 
                  color       = 'gray', 
                  alpha       = 0.5, 
                  linestyle   = '--')
gl.top_labels   = False
gl.right_labels = False
gl.ylabel_style = {'rotation': 90}

###
### Open observation dataset
###
if plot_obs:
    if debug: print("Opening observation file: {}".format(fname_obs))
    df = pd.read_csv(fname_obs)
    df = df.loc[df.dataset=='assimilation']
    ax.scatter(x          = df['longitude'], 
               y          = df['latitude'],
               marker     = 'o',
               s          = 12,
               edgecolors = 'k',
               facecolors = 'None',
#               linewidths = 0.6,
#               alpha      = 0.8,
               label      = "Assimilation dataset (60%)",
               transform  = crs.PlateCarree())
    ax.legend(title="Observation sites:")

###
### Output plot
###
if debug: print("Saving output file: {}".format(fname_out))
plt.savefig(fname_out,dpi=200,bbox_inches='tight')
