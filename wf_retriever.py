"""
AUTHOR: Paarangat Pushkarna 
EMAIL: pushkarnap@student.unimelb.edu.au

Reaches into an HDF file, goes to the specified pulse and waveform, returns.
"""

import argparse 
import h5py
import numpy as np

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
        print(xaxis_raw.shape, yaxis_raw.shape)
        
    
def create_axes(dataset):
    print(dataset.attrs)
    
        
if __name__ == '__main__':
    return_wf(args.filepath, args.pulse, args.channel)    
    

