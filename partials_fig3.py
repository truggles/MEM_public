import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import OrderedDict
import matplotlib.ticker as ticker
import matplotlib as mpl
import matplotlib.tri as tri
#mpl.rcParams['figure.dpi']= 1200

# Added in order of the panels
cases = OrderedDict()
cases['Natural Gas'] = 1
cases['Natural Gas + Solar + Wind'] = 2
cases['Solar + Battery'] = 3
cases['Wind + Battery'] = 4
cases['Solar + Wind + Battery'] = 5

def elongate(df):
    for i, col in enumerate(df.columns):
        if i == 0:
            vect = df[col].values
        else:
            vect = np.append(vect, df[col])
    return vect

dfx = pd.read_csv('partials/x.csv', header=None)
xs = elongate(dfx)
dfy = pd.read_csv('partials/y.csv', header=None)
ys = elongate(dfy)


dfs = {}
for case, f in cases.items():
    df_dx = pd.read_csv(f'partials/dx{cases[case]}.csv', header=None)
    dx = elongate(df_dx)
    dx = np.where(dx == 3, 3.00001, dx)
    df_dy = pd.read_csv(f'partials/dy{cases[case]}.csv', header=None)
    dy = elongate(df_dy)
    dy = np.where(dy == 3, 3.00001, dy)
    df = pd.DataFrame({'x': xs, 'y': ys, 'dx': dx, 'dy': dy})
    
    dfs[case] = df



# Custom matplotlib contour percent formatter
# https://matplotlib.org/stable/gallery/images_contours_and_fields/contour_label_demo.html
# This custom formatter removes trailing zeros, e.g. "1.0" becomes "1", and
# then adds a percent sign.
def fmt(x):
    s = f"{x:.1f}"
    if s.endswith("0"):
        s = f"{x:.0f}"
    return rf"{s}\%" if plt.rcParams["text.usetex"] else f"{s}%"




fig, axs = plt.subplots(ncols=len(cases), nrows=2, sharex=True, sharey=True, figsize=(13, 6))
cmap = mpl.cm.get_cmap('plasma', 512)
cmap.set_over("blue")


i = 0
cntr2sEV1 = []
cntr2sEV2 = []
for case in cases.keys():

    df = dfs[case]

    x = df['x']
    y = df['y']
    z_ev1 = df['dx']
    z_ev2 = df['dy']
    
    # https://matplotlib.org/stable/gallery/images_contours_and_fields/irregulardatagrid.html
    # ----------
    # Tricontour
    # ----------
    levels = np.arange(0, 3.1, .25)
    vmax = 3.
    levels = [0, .5, 1, 1.5, 2, 2.5, vmax]
    axs[0][i].tricontour(x, y, z_ev1, levels=levels, linewidths=.5, colors='k')
    cntr2 = axs[0][i].tricontourf(x, y, z_ev1, levels=levels, cmap=cmap)
    cntr2sEV1.append(cntr2)
    axs[0][i].set(xlim=(0, 1), ylim=(0, 1))
    axs[0][i].yaxis.set_major_locator(ticker.MultipleLocator(.2))
    axs[0][i].xaxis.set_major_locator(ticker.MultipleLocator(.2))
    
    axs[1][i].tricontour(x, y, z_ev2, levels=levels, linewidths=.5, colors='k')
    cntr2 = axs[1][i].tricontourf(x, y, z_ev2, levels=levels, cmap=cmap)
    cntr2sEV2.append(cntr2)
    axs[1][i].set(xlim=(0, 1), ylim=(0, 1))
    axs[1][i].yaxis.set_major_locator(ticker.MultipleLocator(.2))
    axs[1][i].xaxis.set_major_locator(ticker.MultipleLocator(.2))

    print(case)
    if i == 0:
        axs[0][i].set_ylabel("V2G load (kW) / Main load (kW)")
        axs[1][i].set_ylabel("V2G load (kW) / Main load (kW)")
    if i == 2:
        axs[1][i].set_xlabel('V1G load (kW) / Main load (kW)')
    axs[0][i].set_title(case, fontsize=11, fontname='Calibri')

    i += 1

#plt.subplots_adjust(left=0.045, bottom=0.15, top=0.9, right=0.9, wspace=.14)
#cbar_ax = fig.add_axes([0.91, 0.15, 0.015, 0.90 - 0.15])
#cbar = fig.colorbar(cntr2sEV1[-1], cax=cbar_ax)
#cbar.ax.set_ylabel('LCOE / LCOE of system\nwith zero EVs (%)') # v2
#dec = 2
#cbar.ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100, decimals=dec))
#cbar.ax.yaxis.set_major_locator(ticker.FixedLocator([0, 20, 40, 60, 80, 100]))
##plt.savefig('maybe_final_fig3_heatmap_new_EVs.png')


plt.subplots_adjust(left=0.045, bottom=0.15, top=0.9, right=0.9, wspace=.14)
dec = 1
cbar_ax1 = fig.add_axes([0.91, 0.56, 0.015, 0.34])
cbar1 = fig.colorbar(cntr2sEV1[-1], cax=cbar_ax1, extend='max')
cbar1.ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100, decimals=dec))
cbar1.ax.set_ylabel(r'$\partial$ LCOE / $\partial$ V1G'+'\n(% LCOE of system with zero EVs)') # v2
cbar1.ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100, decimals=dec))
cbar1.ax.yaxis.set_major_locator(ticker.MultipleLocator(.5))

cbar_ax2 = fig.add_axes([0.91, 0.15, 0.015, 0.34])
cbar2 = fig.colorbar(cntr2sEV2[-1], cax=cbar_ax2, extend='min')
cbar2.ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100, decimals=dec))
cbar2.ax.set_ylabel(r'$\partial$ LCOE / $\partial$ V2G'+'\n(% LCOE of system with zero EVs)') # v2
cbar2.ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100, decimals=dec))
cbar2.ax.yaxis.set_major_locator(ticker.MultipleLocator(.5))
plt.savefig('maybe_final_fig3_heatmap_partials.png')
