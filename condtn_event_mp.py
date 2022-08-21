import h5py
import numpy as np
import csv
import time
import concurrent.futures
import argparse
from pathlib import Path

CUTOFF_FACTOR = 0.9

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

def do_cutoff(samples, scaled_wf, max_pow, inc):
    
    pow_max_ninety = max_pow * CUTOFF_FACTOR
            
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
        return pw
    except:
        return 0

def wf_proc_psi(wf):
    
    samples = np.arange(wf.attrs["wf_samples"])
    inc = wf.attrs["wf_increment"]
    scaled_wf = scale_pow(wf)
    max_pow = np.amax(scaled_wf)
    pw = do_cutoff(samples, scaled_wf, max_pow, inc)
    
    return (max_pow, pw)

def scrape_info_pulse(pulse):
    
    log = pulse.attrs["Log Type"]
    pc = pulse.attrs["Pulse Count"]
    wf = pulse["PSI_amp"]
    max_pow, pw = wf_proc_psi(wf)
    
    return [pc, log, max_pow, pw]

def scrape_info_file(hdf_file, csv_name):
    
    with h5py.File(hdf_file, "r") as hdf_fhand:
        
        pulses = hdf_fhand.keys()
        
        #GROUP WRITE
        with open(csv_name, "a") as csv_fhand:
            writer = csv.writer(csv_fhand)
            drows = []
            for pulse in pulses:
                drow = scrape_info_pulse(hdf_fhand[pulse])
                drows.append(drow)
            writer.writerows(drows)
            
        #ATOMIC WRITE: seems to be more time consuming from a sample of 10 pulses
        #for pulse in pulses:
            #with open(csv_name, "a") as csv_fhand:
                #writer = csv.writer(csv_fhand)
                #result = scrape_info_pulse(hdf_fhand[pulse])
                #writer.writerow(scrape_info_pulse(hdf_fhand[pulse]))

def do_csv_write(hdf_path, csv_name):
    
    hdf_file_list = list(hdf_path.glob("EventData*_*.hdf"))
    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(scrape_info_file, hdf_file, csv_name) \
            for hdf_file in hdf_file_list]
        for f in concurrent.futures.as_completed(results):
            pass

if __name__ == "__main__":
    
    cli_parser = argparse.ArgumentParser(description = 'Make conditioning plot')
    cli_parser.add_argument('-f', '--folderpath', type=str, metavar='', required = True, 
                        help = 'HDF folderpath')
    cli_parser.add_argument('-c', '--csv_name', type=str, metavar='', required = True, 
                        help = 'Name of csv outfile')
    args = cli_parser.parse_args()
    
    hdf_path = Path(args.folderpath)

    with open(args.csv_name, "w") as csv_fhand:
        fieldnames = ["Pulse Count", "Log Type", "PSI_amp max (scaled)", "PSI pulse width (90pc)"]
        writer = csv.writer(csv_fhand)
        writer.writerow(fieldnames)
    
    start = time.time()
    do_csv_write(hdf_path, args.csv_name)
    took = time.time() - start
    
    print(took)
    
