#import importlib
#tranf_spec = importlib.util.find_spec("src.transformation")
#if tranf_spec is not None:
    #from src.transformation import create_event_ext_link 
    #print("Import successful")
import argparse
from pathlib import Path
from src.transformation import create_event_ext_link

if __name__ == '__main__':
    cli_parser = argparse.ArgumentParser(description = 'Create external links, given existing hdf files')
    cli_parser.add_argument('-f', '--folderpath', type=str, metavar='', required = True, 
                        help = 'HDF folderpath')
    args = cli_parser.parse_args()
    
    hdf_path = Path(args.folderpath)
    
    create_event_ext_link(hdf_path)
