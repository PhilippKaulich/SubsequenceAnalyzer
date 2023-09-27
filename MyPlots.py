# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 07:24:57 2022

@author: Philipp
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 21:08:37 2022

@author: Phili
"""

import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np
import pandas as pd


from collections import Counter    
from matplotlib.ticker import MaxNLocator, FormatStrFormatter
from matplotlib.cm import ScalarMappable
from adjustText import adjust_text
import matplotlib.ticker as mtick


def create_cleavage_site_plot(df):
    ### Parameters 
    df_min = df.min().min()
    df_max = df.max().max()
    df_mean = int((df_max - df_min) / 2)
    
    figure_name = "Cleavage Sites"
    while plt.fignum_exists(figure_name):
        figure_name += "_new"
    plt.figure(figure_name)
    # Placing the plots in the plane
    ax1 = plt.subplot2grid((2, 2), (0, 0))
    ax2 = plt.subplot2grid((2, 2), (1, 1))
    ax3 = plt.subplot2grid((2, 2), (1, 0))
         
    ax1 = sns.barplot(x=list(df.columns), y=list(df.sum()), ax=ax1, color="grey")
    ax1.set(xticklabels=[])
    ax1.tick_params(bottom=False)
    ax1.set_yticks([0,max(list(df.sum()))])
    ax1.set_yticklabels(["", max(list(df.sum()))])
    ax1.set_ylabel("Count")
    
    ax2 = sns.barplot(y=list(df.columns), x=list(df.sum(axis=1)), ax=ax2, 
                      orient = 'h', color="grey")
    ax2.set(yticklabels=[])
    ax2.tick_params(left=False)
    ax2.set_xlabel("Count")
    
    ax2.set_xticks([0,max(list(df.sum(axis=1)))])
    ax2.set_xticklabels(["",max(list(df.sum(axis=1)))])
    
    
    ax3 = sns.heatmap(df, cmap="terrain_r",  cbar=True, xticklabels=True, 
                      yticklabels=True, ax=ax3, 
                      cbar_kws={"shrink": 0.5, "aspect": 5, 
                                "ticks":[0, df_mean, df_max], 
                                "label":"Count"})  # <-- here
    ax3.tick_params(axis='x', rotation=0)
    ax3.set_xlabel(r"X|$\bf{X'}$")
    ax3.set_ylabel(r"$\bf{X}$|X'")
    
    # Drawing the frame
    for _, spine in ax3.spines.items():
        spine.set_visible(True)
        spine.set_linewidth(1)
    
    
    
    #% start: automatic generated code from pylustrator
    plt.figure(figure_name).ax_dict = {ax.get_label(): ax for ax in plt.figure(figure_name).axes}
    plt.figure(figure_name).ax_dict["<colorbar>"].set_facecolor("#ffffffff")
    plt.figure(figure_name).ax_dict["<colorbar>"].set_position([0.737941, 0.762853, 
                                                      0.022157, 0.147638])
    plt.figure(figure_name).axes[0].set_position([0.230218, 0.755994, 0.476001, 0.160053])
    plt.figure(figure_name).axes[0].yaxis.labelpad = -16.796539
    plt.figure(figure_name).axes[0].get_yaxis().get_label().set(position=(263.4382934051522,
        0.5), text='Count', ha='center', va='bottom', fontsize=12.0, rotation=90.0)
    plt.figure(figure_name).axes[1].set_position([0.718318, 0.178629, 0.143573, 0.561219])
    plt.figure(figure_name).axes[1].xaxis.labelpad = -14.717445
    plt.figure(figure_name).axes[1].get_xaxis().get_label().set(position=(0.5000000000000009,
        150.86593315690865), text='Count', ha='center', va='top', fontsize=12.0)
    plt.figure(figure_name).axes[2].set_position([0.230218, 0.178629, 0.476001, 0.561219])
    plt.figure(figure_name).axes[2].get_xaxis().get_label().set(position=(0.5, 
        104.56441090866511), text="X|$\\bf{X'}$", ha='center', va='top', fontsize=14.0)
    plt.figure(figure_name).axes[2].get_yaxis().get_label().set(position=(216.0852489086651, 
        0.5), text="$\\bf{X}$|X'", ha='center', va='bottom', fontsize=14.0, rotation=90.0)
    #% end: automatic generated code from pylustrator
    
    plt.show()
    
    
    

# https://stackoverflow.com/questions/36271302/changing-color-scale-in-seaborn-bar-plot
def _colors_from_values(values, palette_name):
    if len(list(set(values))) == 1: return "black"
    # normalize the values to range [0, 1]
    normalized = (values - min(values)) / (max(values) - min(values))
    # convert to indices
    indices = np.round(normalized * (len(values) - 1)).astype(np.int32)
    # use the indices to get the colors
    palette = sns.color_palette(palette_name, len(values))
    return np.array(palette).take(indices, axis=0)

    



# function to add value labels
def addlabels(x, y, s):
    for i in range(len(x)):
        plt.text(x[i], y[i] + (max(y)/50), s[i], ha = 'center')



def calculate_ticks(max_value):
    if max_value%5 == 0:
        tick_list = [0,max_value/5*1, max_value/5*2, max_value/5*3, max_value/5*4, max_value]
    elif max_value%4 == 0:
        tick_list = [0,max_value/4*1, max_value/4*2, max_value/4*3, max_value]
    elif max_value%3 == 0:
        tick_list = [0,max_value/3*1, max_value/3*2, max_value]
    elif max_value == 2:
        tick_list = [0, 1, 2]
    else:
       tick_list = [0, max_value/2, max_value]
    return tick_list


def _visualize_proteoforms_in_console(ll, protein_sequence):
    print(0, len(protein_sequence), protein_sequence, "", sep="\t")
    for proteoform in ll:
        start_pos, end_pos, seq, npsms = proteoform
        print(start_pos, end="\t")
        print(end_pos, end="\t")
        print("".join(["."]*start_pos), end="")
        print(seq, end="")
        print("".join(["."]*(len(protein_sequence) - end_pos)), end="\t")
        print(npsms, end="\n")


def flat_list(l):
    flat_list = [item for sublist in l for item in sublist]
    return flat_list


def subsequence_visualization(ll=[[1,5,"BVG",9], [2,16,"BVG",2], [5,19,"BVG",10], [3,16,"BVG",7], [4,12,"BVG",5]], protein_sequence="ABDEFGHIKLIJKSDFBNRS", protein_accession="PXSD78"):

    plt.figure(dpi=120)
    
    ll = sorted(ll)
    _visualize_proteoforms_in_console(ll, protein_sequence)
    
    start, end, sequence, psms = list(zip(*ll))
    psms = np.array(psms)
    colors = _colors_from_values(psms, "YlOrRd")
    indices = [i for i in range(len(ll))]
    plt.barh(y=indices, width=[e-s for s,e in zip(start, end)], left=start, color = colors)
    plt.xlabel("AA Position")
    plt.ylabel("Proteoforms")
    plt.title(protein_accession)
    plt.xlim([0, len(protein_sequence)])
    # Colormap
    if type(colors) != str:
        my_cmap = plt.cm.get_cmap('YlOrRd')
        my_cmap(colors)
        sm = ScalarMappable(cmap=my_cmap, norm=plt.Normalize(0, max(psms)))
        sm.set_array([])
        cbar = plt.colorbar(sm)
        tick_list = calculate_ticks(max(psms))
        cbar.set_ticks(tick_list)
        cbar.ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
        cbar.set_label('#PrSMs', rotation=270,labelpad=25)
    
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.gca().xaxis.set_major_locator(MaxNLocator(5, integer=True))
    plt.show()
    
    
        
    protein_sequence = "." + protein_sequence + "."
    #### Proteoform Level
    start, end, _, psms = list(zip(*ll))
    proteoform_distribution(start, end, protein_sequence, protein_accession, "#Proteoforms")
    # PrSMs-gewichtet
    start = flat_list([[i]*j for i, j in zip(start, psms)])
    end = flat_list([[i]*j for i, j in zip(end, psms)])
    proteoform_distribution(start, end, protein_sequence, protein_accession, "#PrSMs")
        
    
    
def proteoform_distribution(start, end, protein_sequence, protein_accession, ylabel="#Proteoforms"):
    plt.figure(dpi=120)
    c_start = dict(Counter(start))
    c_end = dict(Counter(end))
    
    c_start_x, c_start_y = list(c_start.keys()), list(c_start.values())
    plt.bar(c_start_x, c_start_y, label="N-term", color="black", alpha=0.5)
    s = [protein_sequence[pos] + "|" + str(r"$\bf{" + protein_sequence[pos+1] +"}$") for pos in c_start_x]
    addlabels(c_start_x, c_start_y, s)
    
    c_end_x, c_end_y = list(c_end.keys()), list(c_end.values())
    plt.bar(c_end_x, c_end_y, label="C-term", color="red", alpha=0.5)
    s = [str(r"$\bf{" + protein_sequence[pos] +"}$") + "|" +protein_sequence[pos+1] for pos in c_end_x]
    addlabels(c_end_x, c_end_y, s)
    
    plt.xlabel("AA Position")
    plt.ylabel(ylabel)
    plt.title(protein_accession)
    # plt.xlim([0, len(protein_sequence)])
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.gca().xaxis.set_major_locator(MaxNLocator(5, integer=True))

    plt.legend()
    plt.show()
    
    

def truncations_pi_chart(numbers=[1232,2342,651,241]): 
    labels = ["N- and C-term \ntruncation", "N-term truncation", "C-term truncation", "Full length"]
    # sns.set(font_scale = 1.2)
    plt.figure(figsize=(8,8))
    colors = ["yellow", "orangered", "seagreen", "royalblue"]
    colors = [(0.6313725490196078, 0.788235294117647, 0.9568627450980393),
             (1.0, 0.7058823529411765, 0.5098039215686274),
             (0.5529411764705883, 0.8980392156862745, 0.6313725490196078),
             (1.0, 0.996078431372549, 0.6392156862745098)]
    patches, texts, autotexts = plt.pie(
        x=numbers, 
        labels=labels,
        autopct='%1.2f%%',
        textprops={'fontsize': 14},
        colors= colors, #sns.color_palette("pastel"), #colors, #sns.color_palette('Set2'),
        startangle=90,
        wedgeprops={"linewidth": 1, "edgecolor": "black", 'antialiased': True},
        # Add space around only one slice
        explode=[0, 0, 0, 0.12]
    )
    plt.show()
    
    
        
    
    
def plot_methionin_cleaveage(d={'A': 0.9091324200913242, 'C': 0.17857142857142858, 'D': 0.007936507936507936, 'E': 0.017361111111111112, 'F': 0.0, 'G': 0.8554913294797688, 'H': 0.0, 'I': 0.07142857142857142, 'K': 0.0, 'L': 0.0, 'M': 0.0, 'N': 0.0, 'P': 0.8702359346642469, 'Q': 0.004454342984409799, 'R': 0.0, 'S': 0.9242152466367713, 'T': 0.862796833773087, 'V': 0.7871485943775101, 'W': 0.0, 'Y': 0.0}):
    aa_radius = {"A": 0.77, "C": 1.22, "D": 1.43, "E": 1.77, "F": 1.90, 
                 "G": 0.00, "H": 1.78, "I": 1.56, "K": 2.08, "L": 1.54, 
                 "M": 1.80, "N": 1.45, "P": 1.25, "Q": 1.75, "R": 2.38, 
                 "S": 1.08, "T": 1.24, "V": 1.29, "W": 2.21, "Y":2.13}
    all_aa = sorted(d.keys())
    x, y = [], []
    for aa in all_aa:
        x.append(aa_radius[aa])
        y.append(d[aa])
    plt.figure("N-terminal Methionine Excision")
    plt.scatter(x, y, color="black")
    # Loop for annotation of all points
    texts = []
    for i in range(len(x)):
        texts.append(plt.annotate(all_aa[i], (x[i]+0.01, y[i]+0.01), color="red"))
    adjust_text(texts, only_move={'points':'y', 'texts':'y'})#, arrowprops=dict(arrowstyle="->", color='r', lw=0.5))
    plt.gca().set_yticklabels([f'{x:.0%}' for x in plt.gca().get_yticks()]) 
    
    plt.gca().set_yticks([0,0.25,0.50,0.75,1.00])
    plt.gca().set_yticklabels(["0%", "25%", "50%", "75%", "100%"])
    
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)

    plt.title("Start-Methionine Cleavage", fontsize=13)
    plt.xlabel("AA Radius / Å",  fontsize=13)
    plt.ylabel("Methionin Excision",  fontsize=13)
    plt.show()
    
    
def plot_methionin_cleavaege_absolut(d={"A": [12, 12], "B": [2, 12], "C": [12, 2]}):
    df = pd.DataFrame.from_dict(d, orient="index", columns=["Met cleaved", "Met not-cleaved"])
    print(df)
    # plt.figure()
    df.plot.bar(color=["red", "black"])
    
    plt.title("Start-Methionine Cleavage", fontsize=13)
    plt.xlabel("Amino acids",  fontsize=13)
    plt.ylabel("Count", fontsize=13)
    plt.xticks(rotation=0, ha='center')
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)
    plt.legend()
    plt.show()








