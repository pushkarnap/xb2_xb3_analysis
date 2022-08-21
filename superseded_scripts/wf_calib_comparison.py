import argparse 
import h5py
import numpy as np
import matplotlib.pyplot as plt
from dateutil import parser
import time
from wf_retriever import plot_wf, scale_yaxis

def return_raw_max(yaxis_raw):
    positive_flag = np.all(yaxis_raw > 0)
    if positive_flag:
        ADC_max = np.amax(yaxis_raw)
        return ADC_max
    return None

def plot_calib_curve(c0, c1, c2, pulse, channel, ADC_max):
    if not (ADC_max == None):
        ADC_counts = np.linspace(0, ADC_max + 100, int(1e4))
    else:
        ADC_counts = np.linspace(0, 1e4, int(1e4))
    
    power_out = c2*(ADC_counts**2) + c1*(ADC_counts) + c0
    fig, ax = plt.subplots()
    ax.plot(ADC_counts, power_out)
    ax.set(xlabel = "ADC counts",
           ylabel = "Power [Watts]",
           title = f"{channel}")
    ax.grid()
    fig.savefig(f"calib_curves/{pulse}_{channel}_plot_scaled.png")

def extract_raw(dataset):
    yaxis_raw = dataset[:]
    xaxis_raw = np.linspace(0, dataset.attrs["wf_samples"], 
                                dataset.attrs["wf_samples"])
    return xaxis_raw, yaxis_raw

def plot_all_wfs(filepath, pulse):
    
    with h5py.File(filepath, "r") as fhand:
        for channel in fhand[f"{pulse}"]:
            dataset = fhand[f"{pulse}/{channel}"]
            
            xaxis_raw, yaxis_raw = extract_raw(dataset)
            ADC_max = return_raw_max(yaxis_raw)
            yaxis_scaled = scale_yaxis(yaxis_raw, 
                                   dataset.attrs.get("Scale_Coeff_c0", 0),
                                   dataset.attrs.get("Scale_Coeff_c1", 1),
                                   dataset.attrs.get("Scale_Coeff_c2", 0))
            plot_wf(xaxis_raw, yaxis_raw, pulse, channel)
            plot_calib_curve(dataset.attrs.get("Scale_Coeff_c0", 0),
                             dataset.attrs.get("Scale_Coeff_c1", 1), 
                             dataset.attrs.get("Scale_Coeff_c2", 0), 
                             pulse, channel, ADC_max)
    return 

if __name__ == '__main__':
    cli_parser = argparse.ArgumentParser(description = 'Plot event data waveforms')
    cli_parser.add_argument('-f', '--filepath', type=str, metavar='', required = True, 
                        help = 'HDF filepath')
    cli_parser.add_argument('-p', '--pulse', type=str, metavar='', required = True, 
                        help = 'Name of pulse')
    args = cli_parser.parse_args()
    
    plot_all_wfs(args.filepath, args.pulse)
