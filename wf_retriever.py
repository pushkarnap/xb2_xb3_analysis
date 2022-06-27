"""
AUTHOR: Paarangat Pushkarna 
EMAIL: pushkarnap@student.unimelb.edu.au

Reaches into an HDF file, goes to the specified pulse and waveform, returns.
"""

import argparse 
import h5py
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description = 'Plot event data waveforms')
parser.add_argument('-f', '--filepath', type=str, metavar='', required = True, 
                    help = 'HDF filepath')
parser.add_argument('-p', '--pulse', type=str, metavar='', required = True, 
                    help = 'Name of pulse')
parser.add_argument('-c', '--channel', type=str, metavar='', required = True,
                    help = 'Name of channel')

args = parser.parse_args()

def return_wf(filepath, pulse, channel):
    
    with h5py.File(filepath, "r") as fhand:
        dataset = fhand[f"{pulse}/{channel}"]
        yaxis_raw = dataset[:]
        xaxis_raw = np.linspace(0, dataset.attrs["wf_samples"], 
                                dataset.attrs["wf_samples"])
        yaxis_scaled = scale_yaxis(yaxis_raw, 
                                   dataset.attrs["Scale_Coeff_c0"],
                                   dataset.attrs["Scale_Coeff_c1"],
                                   dataset.attrs["Scale_Coeff_c2"])
        plot_wf(xaxis_raw, yaxis_scaled, pulse, channel)
        
    
def scale_yaxis(yaxis, c0, c1, c2):
    scaled = np.abs(c0*(yaxis**2) + c1*yaxis + c2)
    return scaled

def plot_wf(xaxis, yaxis, pulse, channel):
    fig, ax = plt.subplots()
    ax.plot(xaxis, yaxis)
    ax.set(xlabel = "Samples [no unit]",
           ylabel = "Power [kW]",
           title = f"{channel}")
    ax.grid()
    fig.savefig(f"{pulse}_{channel}_plot.png")
    
    
        
if __name__ == '__main__':
    return_wf(args.filepath, args.pulse, args.channel)    
    

