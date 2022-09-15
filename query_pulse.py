import concurrent.futures
import argparse
import h5py
from pathlib import Path
import csv
import numpy as np

def scrape_info_pulse(pulse, feature_list):
    
    row_to_write = []
    for feature in feature_list:
        row_to_write.append(pulse.attrs.get(feature, np.nan))

    return row_to_write

def scrape_info_file(hdf_file, csv_name, feature_list):
    
    try:
        hdf_fhand = h5py.File(hdf_file, "r")
    except:
        print(f"Could not open file {hdf_file}")
        return
    
    pulses = hdf_fhand.keys()
    
    with open(csv_name, "a") as csv_fhand:
        writer = csv.writer(csv_fhand)
        drows = []
        for pulse in pulses:
            drow = scrape_info_pulse(hdf_fhand[pulse], feature_list)
            drows.append(drow)
        writer.writerows(drows)
    
    hdf_fhand.close()
    
    return

def do_csv_write(hdf_path, csv_name, feature_list):
    
    hdf_file_list = list(hdf_path.glob("EventData*_*.hdf"))
    with open(csv_name, "w") as csv_fhand:
        writer = csv.writer(csv_fhand)
        writer.writerow(feature_list)
        
    for hdf_file in hdf_file_list:
        print(hdf_file)
        scrape_info_file(hdf_file, csv_name, feature_list)
    
    #with concurrent.futures.ProcessPoolExecutor() as executor:
        #results = [executor.submit(scrape_info_file, hdf_file, csv_name, feature_list) \
            #for hdf_file in hdf_file_list]
        #for f in concurrent.futures.as_completed(results):
            #pass

if __name__ == "__main__":
    cli_parser = argparse.ArgumentParser(description = 'Retrieve general pulse attributes. Note, this is simple extraction, and no processing or aggregation is undertaken.')
    cli_parser.add_argument('-f', '--filepath', type=str, metavar='', required = True, 
                            help = 'HDF folderpath')
    cli_parser.add_argument('-c', '--csv_name', type=str, metavar='', required = True, 
                            help = 'Name of csv outfile')
    cli_parser.add_argument('-l', '--featurelist', action = 'append', metavar='', required = True,
                            help = 'List of features to scrape, usage -l [feature1] -l [feature2] -l ... etc')
    args = cli_parser.parse_args()
    
    do_csv_write(Path(args.filepath), args.csv_name, args.featurelist)
    
    
    
    
