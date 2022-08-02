import argparse 
from pathlib import Path
import h5py 
import numpy as np
import csv

POWER_THRESH = 650000 #W set by lee millar
CUTOFF_FACTOR = 0.9

def get_filepaths(hdf_path):
    hdf_file_list = list(hdf_path.glob("EventData*_*.hdf"))
    return hdf_file_list

def scale_yaxis(yaxis, c0, c1, c2):
    scaled = c2*(np.square(yaxis)) + c1*yaxis + c0
    return scaled

def scale_pow(wf):
    c0 = wf.attrs.get("Scale_Coeff_c0", 0)
    c1 = wf.attrs.get("Scale_Coeff_c1", 1)
    c2 = wf.attrs.get("Scale_Coeff_c2", 0)
    scaled_wf = scale_yaxis(wf[:].astype('float64'), c0, c1, c2)
    return scaled_wf

def get_sign_change(samples, scaled_wf, pow_max_ninety):
    signs = np.sign(scaled_wf - pow_max_ninety)
    sign_change = (signs[:-1] != signs[1:])
    pre_icept_sple = samples[np.r_[sign_change, [False]]]
    post_icept_sple = samples[np.r_[[False], sign_change]]
    return (pre_icept_sple, post_icept_sple)
    
def psi_file_summ(hdf_file):
    drows = []
    with h5py.File(hdf_file, "r") as hdf_fhand:
        pulses = list(hdf_fhand.keys())
        for pulse in pulses:
            pc = hdf_fhand[pulse].attrs["Pulse Count"]
            wf = hdf_fhand[pulse]["PSI_amp"]
            samples = np.arange(wf.attrs["wf_samples"])
            inc = wf.attrs["wf_increment"]
            
            scaled_wf = scale_pow(wf)
            pow_max = np.amax(scaled_wf)
            if (pow_max < POWER_THRESH):
                continue
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
            
            pw = np.abs(x_icepts[1] - x_icepts[0])
            drow = [pc, pow_max, pw]
            drows.append(drow)
    return drows

def save_condition(hdf_path):
    hdf_files = get_filepaths(hdf_path)
    with open("condtn_psi_data.csv", "w") as csv_fhand:
        fieldnames = ["Pulse Count", "PSI_amp max (scaled)", "PSI pulse width (90pc)"]
        writer = csv.writer(csv_fhand)
        writer.writerow(fieldnames)
    
    for hdf_file in hdf_files:
        with open("condtn_psi_data.csv", "a") as csv_fhand:
            writer = csv.writer(csv_fhand)
            writer.writerows(psi_file_summ(hdf_file))
        print(f"done processing {hdf_file.stem}")
    return
    
if __name__ == '__main__':
    cli_parser = argparse.ArgumentParser(description = 'Make conditioning plot')
    cli_parser.add_argument('-f', '--folderpath', type=str, metavar='', required = True, 
                        help = 'HDF folderpath')
    args = cli_parser.parse_args()
    
    hdf_path = Path(args.folderpath)
    
    save_condition(hdf_path)
