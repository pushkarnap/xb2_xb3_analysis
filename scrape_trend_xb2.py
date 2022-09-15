import argparse 
from pathlib import Path
import h5py 
import numpy as np
import csv
import pickle
from manual_selection import clean_tstamps
import pandas as pd

def scrape_trend(path, flist, csv_name):
    with h5py.File(path, "r") as fhand:
        runs = fhand.keys()
        run_dfs = []
        for run in runs:
            tstamp = flist[0]
            feat = flist[1]
            run_df = pd.DataFrame(data=fhand[run][tstamp], columns=[tstamp])
            if feat in fhand[run].keys():
                run_df[feat] = np.array(fhand[run][feat])
            else:
                print(f"Run {run} was not added to the trend dataset. Missing data.")
                continue
            run_df = clean_tstamps(run_df)
            run_dfs.append(run_df)
        
        if run_dfs:
            pd.concat(run_dfs).to_csv(csv_name, mode = "a", header = False)
        
def scrape_trend_files(path, flist, csv_name):
    
    tfiles = list(path.glob("TrendData*_*.hdf"))
    
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
    cli_parser.add_argument('-l', '--featurelist', action = 'append', metavar='', required = True,
                            help = 'Feature to scrape, usage -l [timestamp] -l [feature] (ONLY ONE FEATURE SUPPORTED, AT A TIME)')
    cli_parser.add_argument('-c', '--csv_name', type=str, metavar='', required = True, 
                            help = 'Name of csv outfile')
    args = cli_parser.parse_args()
    
    scrape_trend_files(Path(args.folderpath), args.featurelist, args.csv_name)
