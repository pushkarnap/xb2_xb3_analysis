import argparse  
import numpy as np
import pandas as pd

POWER_THRESH = 650000 #Watts, as set by Lee Millar (?)
CUTOFF_FACTOR = 0.9

def proc_maxima(csv_name):
    raw_df = pd.read_csv(csv_name)
    thresh_condition = np.array(raw_df["PSI_amp max (scaled)"]) > POWER_THRESH
    culled_df = raw_df[thresh_condition]
    full_df = culled_df.assign(pw_cut = culled_df["PSI_amp max (scaled)"] * CUTOFF_FACTOR)
    full_df.to_csv(f"{csv_name}_procd.csv")

if __name__ == '__main__':
    cli_parser = argparse.ArgumentParser(description = 'Process event maxima')
    cli_parser.add_argument('-f', '--filename', type=str, metavar='', required = True, 
                        help = 'name of csv containing maxima')
    args = cli_parser.parse_args()
    
    csv_name = args.filename
    
    proc_maxima(csv_name)
