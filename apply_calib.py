import argparse 
from pathlib import Path

def get_filepaths(hdf_path):
    return list(hdf_path.glob("EventData*.hdf"))

def run_calib(hdf_path):
    hdf_files = get_filepaths(hdf_path)
    print(hdf_files)
    return

if __name__ == '__main__':
    cli_parser = argparse.ArgumentParser(description = 'Return faulty calibration')
    cli_parser.add_argument('-f', '--folderpath', type=str, metavar='', required = True, 
                        help = 'HDF folderpath')
    args = cli_parser.parse_args()
    
    hdf_path = Path(args.folderpath)
    
    run_calib(hdf_path)
