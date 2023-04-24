import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
import cartopy.crs as crs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
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
fname_out       = 'figures/maps.png'
fname_obs       = config.get(block,'fname_obs')
fname_sh        = config.get(block,'fname_sh')
levels          = config.get(block,'levels')
fname           = "analysis_100.nc"
plot_obs        = False
plot_shape      = True
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

if plot_shape:
    if debug: print("Opening shapefile file: {}".format(fname_sh))
    reader = shpreader.Reader(fname_sh)
    labels = {'0.01cm':  {'lat': -35.60,
                          'lon': -73.1,
                          'name': "0.1"},
              '0.05cm':  {'lat': -37.35,
                          'lon': -72.5,
                          'name': "0.5"},
              '0.1cm':   {'lat': -38.65,
                          'lon': -71.50,
                          'name': "1"},
              '0.2cm':   {'lat': -39.25,
                          'lon': -71.3,
                          'name': "2"},
              '0.4cm_a': {'lat': -40.31,
                          'lon': -71.15,
                          'name': "4"},
              '0.4cm_b': {'lat': -40.65,
                          'lon': -71.65,
                          'name': "4"},
              }

plots = [
    {'label':"(a) Prior ensemble mean",
     'path': 'GNC',
     'field': 'forecast',
     },
    {'label':"(b) EnKF",
     'path': 'ENKF',
     'field': 'analysis',
     },
    {'label':"(c) GNC",
     'path': 'GNC',
     'field': 'analysis',
     },
    {'label':"(d) GIG",
     'path': 'GIG/003',
     'field': 'analysis',
     },
    ]
ncols = 2
nrows = len(plots)//ncols

###
### Plot deposit contours
###
fig, axs = plt.subplots(
        nrows=nrows,
        ncols=ncols,
        subplot_kw={'projection': crs.PlateCarree()},
        sharex=True,
        sharey=True,
        figsize=(12,12)
        )

levels = [float(item) for item in levels.split()]
cmap   = plt.cm.RdYlBu_r
norm   = BoundaryNorm(levels,cmap.N)

for i,item in enumerate(plots):
    path  = item['path']
    field = item['field']
    label = item['label']
    fname_an = join(path,fname) 
    if debug: print("Opening analysis file: {}".format(fname_an))
    ds = xr.open_dataset(fname_an)

    fc = axs.flat[i].contourf(ds.lon,ds.lat,10.0*ds[field],
                     levels = levels,
                     norm = norm,
                     cmap = cmap,
                     extend='max',
                     transform = crs.PlateCarree()
                    )
    axs.flat[i].set_title(label)

# Adjust the location of the subplots on the page to make room for the colorbar
fig.subplots_adjust(bottom  = 0.1,
                    top     = 0.95,
                    left    = 0.05,
                    right   = 0.95,
                    hspace  = 0.05,
                    wspace  = 0.05,
                    )

# Add a colorbar axis at the bottom of the graph
cbar_ax = fig.add_axes([0.2, 0.05, 0.6, 0.02])

# Draw the colorbar
cbar=fig.colorbar(
        fc, 
        ticks       = levels,
        orientation = 'horizontal',
        cax         = cbar_ax,
        )
cbar.set_label('Deposit thickness in mm', fontsize = 16)

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

for ax in axs.flat:
    ax.add_feature(BORDERS, linewidth=0.4)
    ax.add_feature(LAND,zorder=0)
    if plot_shape:
        for item in reader.records():
            ax.add_geometries(item.geometry,
                              crs.PlateCarree(), 
                              facecolor='None', 
                              linewidths=1, 
                              alpha=0.5)

        for key, value in labels.items():
            ax.text(value["lon"],
                    value["lat"],
                    value["name"])

for i in range(nrows):
    for j in range(ncols):
        gl = axs[i,j].gridlines(crs=crs.PlateCarree(),
                          draw_labels = True,
                          linewidth   = 0.5, 
                          color       = 'gray', 
                          alpha       = 0.5, 
                          linestyle   = '--')
        gl.top_labels   = False
        gl.right_labels = False
        gl.ylabel_style = {'rotation': 90}
        if i<nrows-1:
            gl.bottom_labels = False
        if j>0:
            gl.left_labels = False

###
### Output plot
###
if debug: print("Saving output file: {}".format(fname_out))
plt.savefig(fname_out,dpi=200,bbox_inches='tight')
