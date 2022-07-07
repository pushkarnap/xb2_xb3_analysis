import argparse 
from pathlib import Path
import h5py 
import numpy as np
import csv

def get_filepaths(hdf_path):
    hdf_file_list = list(hdf_path.glob("EventData*_*.hdf"))
    return hdf_file_list

def scale_yaxis(yaxis, c0, c1, c2):
    scaled = c2*(np.square(yaxis)) + c1*yaxis + c0
    return scaled

def calc_psi_max(obj):
    psi_adc_max = float(np.amax(obj[:]))
    c0 = obj.attrs.get("Scale_Coeff_c0", 0)
    c1 = obj.attrs.get("Scale_Coeff_c1", 1)
    c2 = obj.attrs.get("Scale_Coeff_c2", 0)
    psi_pow_max = scale_yaxis(psi_adc_max, c0, c1, c2)
    return psi_pow_max

def psi_file_summ(hdf_file):
    drows = []
    with h5py.File(hdf_file, "r") as hdf_fhand:
        pulses = list(hdf_fhand.keys())
        for pulse in pulses:
            pc = hdf_fhand[pulse].attrs["Pulse Count"]
            psi_amp_max = calc_psi_max(hdf_fhand[pulse]["PSI_amp"])
            drow = [pc, psi_amp_max]
            drows.append(drow)
    return drows

def save_condition(hdf_path):
    hdf_files = get_filepaths(hdf_path)
    for hdf_file in hdf_files:
        print(f"processing {hdf_file.stem}")
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
