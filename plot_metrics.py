import pandas as pd
import matplotlib.pyplot as plt
from os.path import join

###
### Parameters
###
dataset    = "validation"
fname_csv  = "validation_metrics.csv"
fname_plt  = "figures/{}_metrics.png".format(dataset)
plot_title = "Evaluation metrics"

plot_items = [
        {'label':"EnKF",
         'marker': "^",
         'ls': 'solid',
         'path': 'ENKF',
         'field': 'analysis',
         },
        {'label':"GNC",
         'marker': "o",
         'ls': 'solid',
         'path': 'GNC',
         'field': 'analysis',
         },
        {'label':"GIG (avg)",
         'marker': "*",
         'ls': 'solid',
         'path': 'GIG',
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
        figsize=(6,nax*3),
        sharex=True
        )
for item in plot_items:
    path    = item['path']
    field   = item['field']
    df   = pd.read_csv(join(path,fname_csv))
    df   = df[(df.percentAss>15) & (df.percentAss<85)]
    y    = df[(df.dataset==dataset) & (df.field==field)]
    #
    for ax,item_ax in zip(axs,plot_axs):
        column = item_ax['column']
        ax.plot(y.percentAss,y[column],
                marker = item['marker'],
                ls     = item['ls'],
                label  = item['label'],
                alpha  = 0.75,
                )

for ax,item_ax in zip(axs,plot_axs):
    if item_ax['column']=='bias':
        x1,x2 = ax.get_ylim()
        bound = max(abs(x1), abs(x2))
        ax.set_ylim(-bound,bound)
    ax.set(ylabel=item_ax['label'])
    ax.grid()

axs[0].legend()
axs[-1].set(xlabel = 'Percent of assimilated data (%)')

fig.suptitle(plot_title)
fig.tight_layout()
fig.savefig(fname_plt,
        dpi=200,
        bbox_inches='tight')
