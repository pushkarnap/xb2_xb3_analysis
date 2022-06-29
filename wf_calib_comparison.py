import argparse 
import h5py
import numpy as np
import matplotlib.pyplot as plt
from dateutil import parser
import time

cli_parser = argparse.ArgumentParser(description = 'Plot event data waveforms')
cli_parser.add_argument('-f', '--filepath', type=str, metavar='', required = True, 
                    help = 'HDF filepath')
cli_parser.add_argument('-p', '--pulse', type=str, metavar='', required = True, 
                    help = 'Name of pulse')

args = cli_parser.parse_args()

with h5py.File(filepath, "r") as fhand:
        pulse_name = fhand[f"{pulse}"]
        print(pulse_name)
        
        
        
        
        
        #yaxis_raw = dataset[:]
        #xaxis_raw = np.linspace(0, dataset.attrs["wf_samples"], 
                                #dataset.attrs["wf_samples"])
        #yaxis_scaled = scale_yaxis(yaxis_raw, 
                                   #dataset.attrs["Scale_Coeff_c0"],
                                   #dataset.attrs["Scale_Coeff_c1"],
                                   #dataset.attrs["Scale_Coeff_c2"])
        #xaxis_reltime = xaxis_timescale(xaxis_raw, dataset.attrs["wf_increment"])
        #plot_wf(xaxis_raw, yaxis_scaled, pulse, channel)
