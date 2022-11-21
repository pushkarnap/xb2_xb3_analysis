import argparse 
from pathlib import Path
import csv
from chprocfuncs import chprocdispatcher
import fcntl

def init_csv(csv_name, scrapename):
    
    with open(csv_name, "w") as csv_fhand:
        
        #fcntl.flock(csv_fhand, fcntl.LOCK_EX)
        
        fieldnames = ["Timestamp", f"{scrapename}"]
        writer = csv.writer(csv_fhand)
        writer.writerow(fieldnames)
        
        #fcntl.flock(csv_fhand, fcntl.LOCK_UN)
        
    return

def appd_csv(csv_name, procfunc, chname, hdf_path):
    
    with open(csv_name, "a") as csv_fhand:
        
        #fcntl.flock(csv_fhand, fcntl.LOCK_EX)
        
        writer = csv.writer(csv_fhand)
        writer.writerows(chprocdispatcher[procfunc](hdf_path, chname))
        
        #fcntl.flock(csv_fhand, fcntl.LOCK_UN)
        
    return
    
def chscrape(hdf_path, csv_name, chname, procfunc, scrapename):
    
    if not csv_name.exists():
        init_csv(csv_name, scrapename)
    appd_csv(csv_name, procfunc, chname, hdf_path)
    
    return

def main():
    
    cli_parser = argparse.ArgumentParser(description = 'Scrape specified channel from given hdf file.')
    cli_parser.add_argument('-f', '--filepath', type=str, metavar='', required = True, 
                        help = 'HDF filepath')
    cli_parser.add_argument('-c', '--csv_name', type=str, metavar='', required = True, 
                        help = 'Name of csv outfile')
    cli_parser.add_argument('-p', '--chname', type=str, metavar='', required = True, 
                            help = 'Name of channel considered')
    cli_parser.add_argument('-s', '--scraperfunc', type=str, metavar='', required = True, 
                            help = 'Name of function to scrape channel info')
    cli_parser.add_argument('-n', '--scrapername', type=str, metavar='', required = True, 
                            help = 'Name of feature scraped')
    args = cli_parser.parse_args()
    
    chscrape(Path(args.filepath), 
             Path(args.csv_name), 
             args.chname, 
             args.scraperfunc, 
             args.scrapername)
    
    return

if __name__ == '__main__':
    main()
