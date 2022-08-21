import argparse 
from pathlib import Path
import h5py 
import numpy as np
import csv
import time

POWER_THRESH = 650000 #W set by lee millar
CUTOFF_FACTOR = 0.9

def get_filepaths(hdf_path):
    #input: file path to directory where HDF files are being stored.
    #To enable looping over different data files. 
    hdf_file_list = list(hdf_path.glob("EventData*_*.hdf"))
    return hdf_file_list

def scale_yaxis(yaxis, c0, c1, c2):
    #input: the raw ADC counts (float64, NOT int16), and scaling constants for raw ADC counts
    #Returns scaled array of power values
    scaled = c2*(np.square(yaxis)) + c1*yaxis + c0
    return scaled

def scale_pow(wf):
    #input: raw ADC counts, int16 format. See above function.
    c0 = wf.attrs.get("Scale_Coeff_c0", 0)
    c1 = wf.attrs.get("Scale_Coeff_c1", 1)
    c2 = wf.attrs.get("Scale_Coeff_c2", 0)
    scaled_wf = scale_yaxis(wf[:].astype('float64'), c0, c1, c2)
    return scaled_wf

def get_sign_change(samples, scaled_wf, pow_max_ninety):
    #input: scaled waveform, 90% cutoff for max power
    #Returns the samples where the 90% cutoff intersects with the pulse.
    signs = np.sign(scaled_wf - pow_max_ninety)
    sign_change = (signs[:-1] != signs[1:])
    pre_icept_sple = samples[np.r_[sign_change, [False]]]
    post_icept_sple = samples[np.r_[[False], sign_change]]
    return (pre_icept_sple, post_icept_sple)
    
def psi_file_summ(hdf_file):
    
    drows = []
    
    #loop over HDF files and each pulse in each HDF file
    #retrieve and process required data
    #write to csv
    #close csv
    #repeat for next pulse and next file...
    
    with h5py.File(hdf_file, "r") as hdf_fhand:
        pulses = list(hdf_fhand.keys())
        for pulse in pulses:
            
            log = hdf_fhand[pulse].attrs["Log Type"]
            pc = hdf_fhand[pulse].attrs["Pulse Count"]
            wf = hdf_fhand[pulse]["PSI_amp"]
            tstamp = hdf_fhand[pulse].attrs["Timestamp"]
            samples = np.arange(wf.attrs["wf_samples"])
            inc = wf.attrs["wf_increment"]
            
            scaled_wf = scale_pow(wf)
            pow_max = np.amax(scaled_wf)
            #if (pow_max < POWER_THRESH):
                #continue
            pow_max_ninety = pow_max * CUTOFF_FACTOR
            
            #get sample numbers straddling both intercepts.
            #s1 pre intercept sample numbers 
            #s2 post intercept sample numbers
            s1, s2 = get_sign_change(samples, scaled_wf, pow_max_ninety)
            
            t1 = s1*inc
            
            y1 = scaled_wf[s1]
            y2 = scaled_wf[s2]
            
            rise = y2 - y1
            m = rise/inc
            factor = pow_max_ninety - y1
            x_icepts = (factor/m) + t1
            
            try:
                pw = np.abs(x_icepts[1] - x_icepts[0])
            except:
                pw = 0
            
            drow = [tstamp, pc, log, pow_max, pw]
            drows.append(drow)
    return drows

def save_condition(hdf_path, csv_name):
    hdf_files = get_filepaths(hdf_path)
    with open(csv_name, "w") as csv_fhand:
        fieldnames = ["Timestamp", "Pulse Count", "Log Type", "PSI_amp max (scaled)", "PSI pulse width (90pc)"]
        writer = csv.writer(csv_fhand)
        writer.writerow(fieldnames)
    
    for hdf_file in hdf_files:
        with open(csv_name, "a") as csv_fhand:
            writer = csv.writer(csv_fhand)
            writer.writerows(psi_file_summ(hdf_file))
        print(f"done processing {hdf_file.stem}")
    return
    
if __name__ == '__main__':
    cli_parser = argparse.ArgumentParser(description = 'Make conditioning plot')
    cli_parser.add_argument('-f', '--folderpath', type=str, metavar='', required = True, 
                        help = 'HDF folderpath')
    cli_parser.add_argument('-c', '--csv_name', type=str, metavar='', required = True, 
                        help = 'Name of csv outfile')
    args = cli_parser.parse_args()
    
    hdf_path = Path(args.folderpath)
    
    start = time.time()
    save_condition(hdf_path, args.csv_name)
    took = time.time() - start
    print(took)
