import pandas as pd
import argparse 
from pathlib import Path
from matplotlib import pyplot as plt

POWER_THRESH = 650000 #Watts

def clean_tstamps(df):
    
    df["Timestamp"] = df["Timestamp"].astype("string").str.split("'").str[1]
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], 
                                     format = "%Y-%m-%dT%H:%M:%S.%fZ", 
                                     utc=True)
    
    return df

def apply_pthresh(df, pchannel):
    
    mask = df[pchannel] > POWER_THRESH
    df_pfilt = df[mask]
    
    return df_pfilt

def plot_condtn(df, start, finish, savename):
    
    df.set_index("Timestamp", inplace=True)
    sample = df.sort_values("Timestamp")[start:end]
    
    fig, ax1 = plt.subplots()
    fig.autofmt_xdate()
    ax2 = ax1.twinx()
    
    ax1.plot(sample["Timestamp"], sample["PSI_amp max (scaled)"]/1e6, 
         color = 'blue', alpha = 0.05, linewidth=0, marker='.',
        markersize = 0.5, rasterized = True)
    ax2.plot(sample["Timestamp"], sample["PSI pulse width (90pc)"]/1e-9,
        color = 'green', alpha = 0.05, linewidth = 0, marker = '.', 
        markersize = 0.5, rasterized = True)
    
    ax1.set_ylabel("Input power to structure (MW)")
    ax2.set_ylabel("Pulse width (ns)")
    ax1.set_xlabel("Time")
    ax1.set_title("CERN TD24BO Line 3: Conditioning")
    
    fig.savefig(f"condtn_out/{savename}")
    
    return 

def visualise(csvpath, start, finish, savename):
    
    df = pd.read_csv(csvpath)
    df = clean_tstamps(df)
    df_pfilt = apply_pthresh(df)
    
    plot_condtn(df_pfilt, start, finish, savename)
    
    return

if __name__ == "__main__":
    cli_parser = argparse.ArgumentParser(description = 'Explore conditioning data on time basis')
    cli_parser.add_argument('-c', '--csvpath', type=str, metavar='', required = True, 
                        help = 'Path of csv infile')
    cli_parser.add_argument('-s', '--start', type=str, metavar='', required = True, 
                        help = 'str of start time in std utc format')
    cli_parser.add_argument('-f', '--finish', type=str, metavar='', required = True, 
                        help = 'str of finish time in std utc format')
    cli_parser.add_argument('-n', '--savename', type=str, metavar='', required = True, 
                        help = 'Name of saved image. jpeg is better than png')
    args = cli_parser.parse_args()
    
    visualise(Path(args.csvpath), args.start, args.finish, args.savename)
