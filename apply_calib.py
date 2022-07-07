import argparse 
from pathlib import Path
import h5py 
import numpy as np

def get_filepaths(hdf_path):
    hdf_file_list = list(hdf_path.glob("EventData*_*.hdf"))
    return hdf_file_list

def scale_yaxis(yaxis, c0, c1, c2):
    scaled = c2*(np.square(yaxis)) + c1*yaxis + c0
    return scaled

def check_psi_scaling(name, obj):
    is_dataset = isinstance(obj, h5py.Dataset)
    if is_dataset:
        is_psi = (obj.attrs["NI_ChannelName"] == "PSI_amp")
        if is_psi:
            psi_adc = obj[:]
            psi_adc = psi_adc.astype('float128')
            c0 = obj.attrs.get("Scale_Coeff_c0", 0)
            c1 = obj.attrs.get("Scale_Coeff_c1", 1)
            c2 = obj.attrs.get("Scale_Coeff_c2", 0)
            psi_scaled = scale_yaxis(psi_adc, c0, c1, c2)
            positive_flag = np.all(psi_scaled >= 0)
                
    return None

def retrieve_adc(hdf_file):
    
    with h5py.File(hdf_file, "r") as fhand:
        fhand.visititems(check_psi_scaling)
    
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
