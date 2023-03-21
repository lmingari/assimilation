import numpy as np
from assimilation import GIG as AssimilationMethod
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
block           = 'GIG'
path_obs        = config.get('DATA','path')
path            = config.get(block,'path')
fname_ens       = config.get(block,'fname_ens')
bulk_density    = config.getfloat(block,'bulk_density')
thickness_min   = config.getfloat(block,'thickness_min')
nsample         = config.getint(block,'nsample')
random_sort     = True
debug           = True

###
### Information screen
###
if debug:
    print("""
    ---------------------------------
    Assimilation using the GIG method
    ---------------------------------
    Input parameters:
    bulk density = {bulk_density} kg/m3
    minimum thickness = {thickness_min} cm
    number of realisations = {nsample}
    using random sorting: {random_sort}
    """.format(bulk_density  = bulk_density,
               thickness_min = thickness_min,
               nsample       = nsample,
               random_sort   = random_sort)
          )

###
### Use the GIG (sequential) method
###
data = AssimilationMethod(thickness_min)

###
### Read model data
###
if debug: print("Opening simulation output file: {}".format(fname_ens))
data.read_ensemble(fname_ens,bulk_density)

for percentAss in np.arange(10,105,5):
    ####
    #### Read obs data
    ####
    fname_obs = "deposit_{:03d}.csv".format(percentAss)
    fname_obs = join(path_obs,fname_obs)
    if debug: print("Opening observation file: {}".format(fname_obs))
    data.read_observations(fname_obs,random_sort=random_sort)
    if debug: print("Number of observations: {}".format(data.nobs))

    ###
    ### Interpolation to observation sites
    ###
    if debug: print("Performing interpolations")
    data.apply_ObsOp()

    for isample in range(nsample):
    ###
    ### Assimilate
    ###
        if debug: print("Assimilating data")
        data.assimilate()

    ###
    ### Save analysis data
    ###
        fname_an = "analysis_{:03d}.nc".format(percentAss)
        fname_an = join(path,"{:03d}".format(1+isample),fname_an)
        if debug: print("Saving analysis output file: {}".format(fname_an))
        data.to_netcdf(fname_an)
