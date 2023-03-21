import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from os.path import join

###
### Parameters
###
dataset   = "validation"
fname_csv = "validation_metrics.csv"
fname_plt = "figures/{}_metrics.png".format(dataset)

if dataset == "assimilation":
    plot_title = "Metrics - Assimilation dataset"
else:
    plot_title = "Metrics - Validation dataset"

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
         'path': 'GIG',
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

plot_axs = [
        {'column': 'rmse',
         'label': 'RMSE'
         },
        {'column': 'bias',
         'label': 'Bias'
         },
        {'column': 'smape',
         'label': 'SMAPE [%]'
         },
        {'column': 'hits',
         'label': 'Hit percent [%]'
         },
        ]
nax = len(plot_axs)

###
### Plot validation metrics
###
fig, axs = plt.subplots(nax,
        figsize=(8,nax*4),
        sharex=True
        )
for item in plot_items:
    path    = item['path']
    field   = item['field']
    df   = pd.read_csv(join(path,fname_csv))
    y    = df[(df.dataset==dataset) & (df.field==field)]
    #
    for ax,item_ax in zip(axs,plot_axs):
        column = item_ax['column']
        ax.set(ylabel=item_ax['label'])
        ax.grid()
        ax.xaxis.set_minor_locator(MultipleLocator(5))
        ax.plot(y.percentAss,y[column],
                marker = item['marker'],
                ls     = item['ls'],
                label  = item['label']
                )

axs[0].legend()
axs[-1].set(xlabel = 'Percent of assimilated data (%)',xlim = (0,100))

fig.suptitle(plot_title)
fig.tight_layout()
fig.savefig(fname_plt,
            dpi=200,
            bbox_inches='tight')
