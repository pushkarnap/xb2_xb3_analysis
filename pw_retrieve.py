import argparse 
from pathlib import Path
import h5py 
import numpy as np
import csv

def get_filepaths(hdf_path):
    hdf_file_list = list(hdf_path.glob("TrendData*.hdf"))
    return hdf_file_list

def write_trend_csv(hdf_file):
    
    with h5py.File(hdf_file, "r") as hdf_fhand:
        runs = list(hdf_fhand.keys())
        for run in runs:
            pc1 = hdf_fhand[run]["Pulse Count 1"]
            pc2 = hdf_fhand[run]["Pulse Count 2"]
            pw1 = hdf_fhand[run]["1PSI_amp pulse width"]
            pw2 = hdf_fhand[run]["2PSI_amp pulse width"]
            dlist = [pc1, pc2, pw1, pw2]
            
            drows = np.stack(dlist, axis = 0)
            drows = np.transpose(drows)
            
            with open("condtn_psi_data_trend.csv", "a") as csv_fhand:
                writer = csv.writer(csv_fhand)
                writer.writerows(drows.tolist())

def create_trend_csv(hdf_path):
    hdf_files = get_filepaths(hdf_path)
    with open("condtn_psi_data_trend.csv", "w") as csv_fhand:
        fieldnames = ["Pulse Count 1", "Pulse Count 2", "Pulse Width 1", "Pulse Width 2"]
        writer = csv.writer(csv_fhand)
        writer.writerow(fieldnames)
    
    for hdf_file in hdf_files:
        write_trend_csv(hdf_file)
        print(f"done processing {hdf_file.stem}")
    return
    
if __name__ == '__main__':
    cli_parser = argparse.ArgumentParser(description = 'Make conditioning plot')
    cli_parser.add_argument('-f', '--folderpath', type=str, metavar='', required = True, 
                        help = 'HDF folderpath')
    args = cli_parser.parse_args()
    
    hdf_path = Path(args.folderpath)
    
    create_trend_csv(hdf_path)
