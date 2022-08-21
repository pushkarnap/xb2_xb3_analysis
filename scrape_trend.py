import argparse 
from pathlib import Path
import h5py 
import numpy as np
import csv
import pickle

def scrape_trend(path, flist, csv_name):
    
    with h5py.File(path, "r") as fhand:
        runs = fhand.keys()
        for run in runs:
            
            feats = []
            for f in flist:
                feats.append(np.array(fhand[run][f]))
            
            with open(csv_name, "a") as csv_fhand:
                writer = csv.writer(csv_fhand)
                writer.writerows(np.array(feats).transpose().tolist())
                

def scrape_trend_files(path, pke, flist, csv_name):
    
    tfiles = 0
    with open(pke, "rb") as phand:
        tfiles = pickle.load(phand)
        
    with open(csv_name, "w") as csv_fhand:
        writer = csv.writer(csv_fhand)
        writer.writerow(flist)
    
    for tfile in tfiles:
        print(path/tfile)
        scrape_trend(path/tfile, flist, csv_name)
    
if __name__ == '__main__':    
    cli_parser = argparse.ArgumentParser(description = 'Scrape trend data')
    cli_parser.add_argument('-f', '--folderpath', type=str, metavar='', required = True, 
                        help = 'HDF folderpath')
    cli_parser.add_argument('-p', '--pickletrend', type=str, metavar='', required = True,
                            help = 'Pickle file specifying the files to be scraped')
    cli_parser.add_argument('-l', '--featurelist', action = 'append', metavar='', required = True,
                            help = 'List of features to scrape, usage -l [feature1] -l [feature2] -l ... etc')
    cli_parser.add_argument('-c', '--csv_name', type=str, metavar='', required = True, 
                            help = 'Name of csv outfile')
    args = cli_parser.parse_args()
    
    scrape_trend_files(Path(args.folderpath), args.pickletrend, args.featurelist, args.csv_name)
