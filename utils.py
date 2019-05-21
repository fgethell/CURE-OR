import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import to_hex

def plot_challenging_types(df_list, df_names, result_path, cTypes):

    ## Plot style
    legend = []
    for i in cTypes.keys()[1:9]: legend.append(cTypes[i][3:].title())
    colorList = cm.rainbow(np.linspace(1,0,len(legend)+1)) #Set2
    dashList = [(10,10),(7,10),(20,3,10,3),(20,5),(20,20),(5,2,8,5),(10,5),(10,10,5,5)]
    lineSList = ['-','-.',':','--','-.','--','-','--']
    lineWList = [2,4,4,4,2,4,4,4] #lineWList[i-1]
    markerList = ['s','>','<','p','H','d','h','*']

    levN = 6
    for df, name in zip(df_list, df_names):
        plt.figure(figsize=(7,5.8))
        for i in cTypes.keys()[1:9]:
            df.iloc[i-1,:levN].plot(color=to_hex(colorList[i-1]),linestyle=lineSList[i-1],\
                                    linewidth=3,dashes=dashList[i-1],marker=markerList[i-1],\
                                    markersize=8)
            plt.legend(legend, fontsize=13, labelspacing=0.7, borderpad=0.37, borderaxespad=0.2,\
                handletextpad=0.1, loc='center left', bbox_to_anchor=(1,0.5))
            # plt.title('Color Images', fontsize=20)
        plt.xlabel('Challenge Levels', fontsize=20, fontweight='normal')
        plt.xticks(range(levN), range(levN), fontsize=16)
        plt.xlim([-0.1,levN-0.9])

        plt.ylabel('Top-5 Accuracy (%%)', fontsize=20, fontweight='normal')
        plt.yticks(fontsize=16)
        plt.ylim([0,50])

        plt.savefig(os.path.join(result_path, 'Plots', name+'.jpg'), bbox_inches='tight')
        plt.close()


def plot_challenging_types_cf(df_list, app, result_path):
    for levCT, cfMat in enumerate(df_list):
        if levCT == 0: numImgs = float(23 * 5 * 5 * 5 * 2)
        elif levCT == 5: numImgs = float(23 * 5 * 5 * 5 * 2 * 7)
        else: numImgs = float(23 * 5 * 5 * 5 * 2 * 8)

        tmps = cfMat[cfMat.columns[:-1]].values/numImgs*100
        tmpMax = max([t for tmp in tmps for t in tmp])

        if levCT == 0: maxVal = tmpMax
        else:
            if tmpMax > maxVal: maxVal = tmpMax

        plt.pcolor(cfMat[cfMat.columns[:-1]].values/numImgs*100, cmap='Blues', vmax=maxVal)

        cbar = plt.colorbar()
        cbar.ax.tick_params(labelsize=13)
        ax = plt.gca()
        ax.invert_yaxis()
        tickLoc = [x + 0.5 for x in range(6)]

        plt.xlabel('Predicted category', fontsize=20, fontweight='normal')
        plt.xticks(tickLoc, range(1,7), fontsize=16)

        plt.ylabel('Actual category', fontsize=20, fontweight='normal')
        plt.yticks(tickLoc, range(1,7), fontsize=16)

        plt.savefig(result_path + '/Plots/%s_lev%d_top1_cf.jpg'%(app, levCT),bbox_inches='tight')
        plt.close()

def scatter_plot_IQA(IQA_vals, perf_vals, result_path):
    markers = ['H','X','o','D','>','P']
    mkSize = 140
    mkSizes = [mkSize-20 if m =='o' else mkSize-60 if m=='D' else mkSize for m in markers]
    mkLineWidth = 1
    maxVals = [55,1,1,1]
    IQAs = ['PSNR', 'SSIM', 'UNIQUE']
    legend = ['Original', 'Level 1', 'Level 2', 'Level 3', 'Level_4', 'Level_5']
    colors = cm.rainbow(np.linspace(0,1,len(legend))) 
    plots = ()

    for IQA in range(len(IQAs)):
        plt.figure(figsize=(3,3))
        for i in range(len(legend)): # lev 0-5
            plot = plt.scatter(IQA_vals.iloc[i, IQA*15:(IQA+1)*15], perf_vals.iloc[i, IQA*15:(IQA+1)*15],
                               mkSizes[i], marker=markers[i], c=colors[i], linewidths=mkLineWidth,
                               edgecolors='k')
            plots += (plot, )
        plt.xlabel(IQAs[IQA], fontsize=17, fontweight='normal', labelpad=10)
        plt.xticks(fontsize=14)

        plt.ylabel('Top-5 Accuracy', fontsize=16, fontweight='normal')
        yMax = 40
        yInc = 10
        ytickLabels = ['%d'%i for i in range(0,yMax, yInc)]
        ytickLabels.append('%i+'%yMax)
        plt.yticks(range(0,yMax+1,yInc), ytickLabels, fontsize=14)
        plt.ylim([0,yMax])
        plt.tight_layout()
        plt.savefig(os.path.join(result_path, 'Plots', 'IQAs_perf_%s.jpg'%IQAs[IQA]))
        plt.close()

    plt.figure(figsize=(9,0.1))
    plt.legend(plots, legend, ncol=len(legend), fontsize='large', frameon=True, loc='center',
               columnspacing=0.5, handletextpad=0.1, borderpad=0.5)
    plt.axis('off')
    plt.savefig(os.path.join(result_path, 'Plots', 'IQAs_perf_legend.jpg'), bbox_inches='tight')
    plt.close()


# TODO
# def plot_acquisition_conditions():
# def scatter_plot_similarity_estimation():
