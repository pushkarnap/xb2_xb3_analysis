import argparse 
from pathlib import Path
import h5py 

def get_filepaths(hdf_path):
    hdf_file_list = list(hdf_path.glob("EventData*_*.hdf"))
    return hdf_file_list

def retrieve_adc(hdf_file):
    
    with h5py.File(hdf_file, "r") as fhand:
        print(f"Hello file! {hdf_file}")
    
def run_calib(hdf_path):
    hdf_files = get_filepaths(hdf_path)
    for hdf_file in hdf_files:
        retrieve_adc(hdf_file)
    return

if __name__ == '__main__':
    cli_parser = argparse.ArgumentParser(description = 'Return faulty calibration')
    cli_parser.add_argument('-f', '--folderpath', type=str, metavar='', required = True, 
                        help = 'HDF folderpath')
    args = cli_parser.parse_args()
    
    hdf_path = Path(args.folderpath)
    
    run_calib(hdf_path)
