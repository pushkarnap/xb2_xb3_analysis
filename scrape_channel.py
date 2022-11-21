import argparse 
from pathlib import Path
import csv
from chprocfuncs import chprocdispatcher

def get_filepaths(hdf_path):
    #input: file path to directory where HDF files are being stored.
    #To enable looping over different data files. 
    hdf_file_list = list(hdf_path.glob("EventData*_*.hdf"))
    return hdf_file_list

def chscrape(hdf_path, csv_name, chname, procfunc, scrapename):
    
    hdf_files = get_filepaths(hdf_path)
    with open(csv_name, "w") as csv_fhand:
        fieldnames = ["Timestamp", f"{scrapename}"]
        writer = csv.writer(csv_fhand)
        writer.writerow(fieldnames)
    
    for hdf_file in hdf_files:
        with open(csv_name, "a") as csv_fhand:
            writer = csv.writer(csv_fhand)
            writer.writerows(chprocdispatcher[procfunc](hdf_file, chname))
    return

if __name__ == '__main__':
    
    cli_parser = argparse.ArgumentParser(description = 'Custom channel scraper')
    cli_parser.add_argument('-f', '--folderpath', type=str, metavar='', required = True, 
                        help = 'HDF folderpath')
    cli_parser.add_argument('-c', '--csv_name', type=str, metavar='', required = True, 
                        help = 'Name of csv outfile')
    cli_parser.add_argument('-p', '--chname', type=str, metavar='', required = True, 
                            help = 'Name of channel considered')
    cli_parser.add_argument('-s', '--scraperfunc', type=str, metavar='', required = True, 
                            help = 'Name of function to scrape channel info')
    cli_parser.add_argument('-n', '--scrapername', type=str, metavar='', required = True, 
                            help = 'Name of feature scraped')
    args = cli_parser.parse_args()
    
    hdf_path = Path(args.folderpath)
    
    chscrape(hdf_path, args.csv_name, args.chname, args.scraperfunc, args.scrapername)
