import argparse 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def csv_unbox(csvname):
    condtn_mat = pd.read_csv(csvname, header = None).to_numpy()
    return condtn_mat

def create_condition_plot(xpts, ypts, labels):
    
    fig, ax = plt.subplots()
    plt.title(labels["title"])
    ax.plot(xpts, ypts, marker = ",", linewidth = 0,
            color = labels["color"], alpha = labels["alpha"])
    ax.set_xlabel(labels["xlabel"])
    ax.set_ylabel(labels["ylabel"])
    fig.savefig(labels["savename"])

    return

def plot_condtn(csvname):
    condtn_mat = csv_unbox(csvname)
    
    label_dict = {
    "title": "Conditioning plot for Line 1 in XBOX3 data",
    "color": "blue",
    "alpha": 0.015,
    "xlabel": "Pulse Count",
    "ylabel": "Max input power to structure [W]",
    "savename": "condition1_p.png"
    }
    
    create_condition_plot(condtn_mat[:, 0], condtn_mat[:, 1], label_dict)
    
    return

if __name__ == '__main__':
    cli_parser = argparse.ArgumentParser(description = 'Make conditioning plot')
    cli_parser.add_argument('-c', '--csvname', type=str, metavar='', required = True, 
                        help = 'Name of csv holding data')
    args = cli_parser.parse_args()
    
    plot_condtn(args.csvname)
    
