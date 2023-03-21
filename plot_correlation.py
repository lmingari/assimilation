import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from os.path import join

###
### Parameters
###
fname_csv = "correlation.csv"
fname_plt = "figures/correlation.png"

plot_items = [
        {'label':"GNC",
         'marker': "*",
         'ls': 'solid',
         'path': 'GNC',
         'field': 'analysis',
         },
        {'label':"GIG",
         'marker': "o",
         'ls': 'None',
         'path': 'GIG/001',
         'field': 'analysis',
         },
        {'label':"EnKF",
         'marker': "^",
         'ls': 'solid',
         'path': 'ENKF',
         'field': 'analysis',
         },
#        {'label':"Forecast",
#         'marker': "s",
#         'ls': 'solid',
#         'path': 'GNC',
#         'field': 'forecast',
#         },
        ]

###
### Plot Correlation coefficient
###
fig, ax = plt.subplots()
for item in plot_items:
    path    = item['path']
    field   = item['field']
    df   = pd.read_csv(join(path,fname_csv))
    y    = df[df.field==field]
    print(y)
    #
    ax.plot(y.percentAss,y.correlation,
            marker = item['marker'],
            ls     = item['ls'],
            label  = item['label']
            )

ax.set(xlabel = 'Percent of assimilated data (%)',
       ylabel = 'Correlation coefficient',
       xlim   = (0,100),
       )
ax.legend()
ax.grid()
ax.xaxis.set_minor_locator(MultipleLocator(5))

#fig.suptitle(plot_title)
fig.tight_layout()
fig.savefig(fname_plt,
            dpi=200,
            bbox_inches='tight')
