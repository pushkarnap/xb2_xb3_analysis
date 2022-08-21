import concurrent.futures
import argparse
import h5py
from pathlib import Path
import csv

def scrape_info_pulse(pulse, hdf_file):
    
    row_to_write = []
    row_to_write.append(pulse.attrs["Timestamp"])
    row_to_write.append(hdf_file.stem)
        
    return row_to_write

def scrape_info_file(hdf_file, csv_name):
    
    with h5py.File(hdf_file, "r") as hdf_fhand:
        
        pulses = hdf_fhand.keys()
        
        with open(csv_name, "a") as csv_fhand:
            writer = csv.writer(csv_fhand)
            drows = []
            for pulse in pulses:
                drow = scrape_info_pulse(hdf_fhand[pulse], hdf_file)
                drows.append(drow)
            writer.writerows(drows)

def do_csv_write(hdf_path, csv_name):
    
    hdf_file_list = list(hdf_path.glob("EventData*_*.hdf"))
    with open(csv_name, "w") as csv_fhand:
        writer = csv.writer(csv_fhand)
        writer.writerow(["Timestamp", "FileName"])
        
    for hdf_file in hdf_file_list:
        scrape_info_file(hdf_file, csv_name)
    
    #with concurrent.futures.ProcessPoolExecutor() as executor:
        #results = [executor.submit(scrape_info_file, hdf_file, csv_name, feature_list) \
            #for hdf_file in hdf_file_list]
        #for f in concurrent.futures.as_completed(results):
            #pass

if __name__ == "__main__":
    cli_parser = argparse.ArgumentParser(description = 'Retrieve timestamps and filepaths of each pulse. Note, this is simple extraction, and no processing or aggregation is undertaken.')
    cli_parser.add_argument('-f', '--filepath', type=str, metavar='', required = True, 
                            help = 'HDF folderpath')
    cli_parser.add_argument('-c', '--csv_name', type=str, metavar='', required = True, 
                            help = 'Name of csv outfile')
    args = cli_parser.parse_args()
    
    do_csv_write(Path(args.filepath), args.csv_name)
    
    
    
    
