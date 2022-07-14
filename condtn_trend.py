import argparse 
from pathlib import Path
import h5py 
import numpy as np
import csv

def get_filepaths(hdf_path):
    hdf_file_list = list(hdf_path.glob("TrendData*.hdf"))
    return hdf_file_list

def psi_file_summ_trend(hdf_file):
    with h5py.File(hdf_file, "r") as hdf_fhand:
        runs = list(hdf_fhand.keys())
        for run in runs:
            with open("condtn_psi_data_trendA.csv", "a") as csv_fhand:
                writer = csv.writer(csv_fhand)
                
                pcs = hdf_fhand[run]["Pulse Count 1"]
                pws = hdf_fhand[run]["1PSI_amp pulse width"]
                
                pcs = np.reshape(pcs, (pcs.shape[0], 1))
                pws = np.reshape(pws, (pws.shape[0], 1))
                drows = np.concatenate((pcs, pws), axis = 1)
                drows = drows.tolist()
                
                writer.writerows(drows)
            
def save_condition(hdf_path):
    hdf_files = get_filepaths(hdf_path)
    for hdf_file in hdf_files:
        print(f"processing {hdf_file.stem}")
        psi_file_summ_trend(hdf_file)
        print(f"done processing {hdf_file.stem}")
    return
    
if __name__ == '__main__':    
    cli_parser = argparse.ArgumentParser(description = 'Make conditioning plot')
    cli_parser.add_argument('-f', '--folderpath', type=str, metavar='', required = True, 
                        help = 'HDF folderpath')
    args = cli_parser.parse_args()    
    hdf_path = Path(args.folderpath)    
    save_condition(hdf_path)
