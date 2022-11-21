import argparse
import pandas as pd
import fastparquet as fp
from pathlib import Path

def merge(folderpath, outpath, keyname):
    
    csvfiles = folderpath.glob("xbox*.csv")
    init_file = next(csvfiles)
    full_df = pd.read_csv(init_file).dropna()
    
    for csvfile in csvfiles:
        full_df = full_df.merge(pd.read_csv(csvfile).dropna(),
                                how="inner",
                                on=["Timestamp",],
                                validate="one_to_one")
        print(csvfile.stem)
        
    full_df.to_parquet(outpath)
    
    return

def main():
    
    cli_parser = argparse.ArgumentParser(
        description = 'Merge csv files in specified folder')
    cli_parser.add_argument('-f', '--folderpath', type=str, 
                            metavar='', required = True, 
                            help = 'csv folderpath')
    cli_parser.add_argument('-o', '--outpath', type=str, 
                            metavar='', required = True, 
                            help = 'path of outfile')
    cli_parser.add_argument('-k', '--keyname', type=str, 
                            metavar='', required = True, 
                            help = 'name of key on which to merge')
    args = cli_parser.parse_args()
    
    merge(Path(args.folderpath), Path(args.outpath), args.keyname)
    
    return

if __name__ == "__main__":
    main()
