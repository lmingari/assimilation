import pandas as pd
from os.path import join
from configparser import ConfigParser

###
### Read configuration file
###
config = ConfigParser(inline_comment_prefixes="#")
config.read('../config.ini')

###
### Parameters
###
block           = 'GIG'
path_obs        = config.get('DATA','path')
path            = config.get(block,'path')
nsample         = config.getint(block,'nsample')
fname_csv       = 'correlation.csv'
#fname_csv       = 'validation_metrics.csv'

frames = []
for isample in range(nsample):
    fname = join(f'{isample+1:03d}',fname_csv)
    frames.append( pd.read_csv(fname) )
df = pd.concat(frames)

#result = df.groupby(['percentAss','dataset','field']).mean()
result = df.groupby(['percentAss','field']).mean()
result.to_csv(fname_csv)
