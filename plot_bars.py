import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from os.path import join

###
### Parameters
###
fname_csv  = "validation_metrics.csv"
fname_plt  = "figures/metric_bars.png"

plot_bars = [
        {'label': "Forecast",
         'path':  'GNC',
         'field': 'forecast',
         },
        {'label': "EnKF",
         'path':  'ENKF',
         'field': 'analysis',
         },
        {'label': "GNC",
         'path':  'GNC',
         'field': 'analysis',
         },
        {'label': "GIG (avg)",
         'path':  'GIG',
         'field': 'analysis',
         },
        ]

plot_subbar = [
        {'index': (60,'assimilation'),
         'label': "Assimilation dataset (60%)",
         'color': 'olivedrab'},
        {'index': (60,'validation'),
         'label': "Validation dataset (40%)",
         'color': 'chocolate'},
        ]

plot_axs = [
        {'column': 'rmse',
         'label': 'RMSE',
         'title': '(a)',
         },
        {'column': 'bias',
         'label': 'MBE',
         'title': '(b)',
         },
        {'column': 'smape',
         'label': 'SMAPE [%]',
         'title': '(c)',
         },
        {'column': 'hits',
         'label': ' 1-to-3 Ratio Band Score [%]',
         'title': '(d)',
         },
        ]
nax = len(plot_axs)

frames = []
for bar in plot_bars:
    path  = bar['path']
    field = bar['field']
    label = bar['label']
    df    = pd.read_csv(join(path,fname_csv))
    df    = df[df.field==field]
    df['label'] = label
    frames.append(df)
df = pd.concat(frames)
df.set_index(['percentAss','dataset'], inplace=True)
df.sort_index(inplace = True)

def minarg(df,column):
    if column=='bias':
        index = df[column].abs().argmin()
    elif column=='hits':
        index = df[column].argmax()
    else:
        index = df[column].argmin()
    return index

###
### Plot bars
###
width = 0.35
ncol = 2
nrow = nax//ncol
if nax%ncol != 0: nrow += 1
fig, axs = plt.subplots(ncols=ncol,nrows=nrow,figsize=(12,10))
for i,item_ax in enumerate(plot_axs):
    ax = axs.flat[i]
    column = item_ax['column']
    label  = item_ax['label']
    title  = item_ax['title']
    for j,bar in enumerate(plot_subbar):
        y = df.loc[bar['index']]
        x = np.arange(len(y)) 
        bars = ax.bar(x+width*(j-0.5),y[column],
                      width=0.9*width,
                      color=bar['color'],
                      label=bar['label'],
                      )
        bl = ax.bar_label(bars,
                          fmt='{:.1f}',
                          padding=4,
                          fontsize=9)
        props = dict(boxstyle='round,pad=0.2', 
                     facecolor=bar['color'], 
                     alpha=0.7)
        imin = minarg(y,column)
        bl[imin].set(bbox=props)

    ax.set_xticks(x, y.label)
    ax.set(ylabel=label, title=title)
    ax.grid(axis='y',
            linestyle='--', 
            linewidth=0.5)

axs[0,0].set(ylim = (0,10))
axs[0,1].set(ylim = (-6,1))
axs[1,0].set(ylim = (0,60))
axs[1,1].set(ylim = (0,90))
axs[0,0].legend()

plt.savefig(fname_plt,
        dpi=200,
        bbox_inches='tight')
