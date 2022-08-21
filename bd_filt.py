import pandas as pd
import numpy as np
import datetime as dt
import argparse
from manual_selection import clean_tstamps, apply_pthresh, POWER_THRESH
import pickle

def filter_by_date(df, segments):
    
    df_filt = pd.DataFrame(columns = list(df.columns))
    
    for segment in segments:
        seg_start, seg_end = segment
        seg_define = (df["Timestamp"] > seg_start) & (df["Timestamp"] < seg_end)
        df_seg = df.loc[seg_define]
        df_filt = pd.concat([df_filt, df_seg])
    
    df_filt.sort_values("Timestamp", inplace=True)
    df_filt.reset_index(drop=True, inplace=True)
    
    return df_filt

def filter_to_bd(csvinpath, picklefile):
    
    df = pd.read_csv(csvinpath)
    df = clean_tstamps(df)
    df_pfilt = apply_pthresh(df)
    
    segments = []
    with open(picklefile, "rb") as fhand:
        segments = pickle.load(fhand)
        
    df_pdfilt = filter_by_date(df_pfilt, segments)
    df_PowerDateBD_filt = df_pdfilt[df_pdfilt["Log Type"] == 2]
    
    return df_PowerDateBD_filt

def merge_with_flags(bd_df, flag_df):
    
    merged = bd_df.merge(flag_df, how="inner", on="Timestamp")
    merged_sorted = merged.sort_values("Timestamp")
    
    return merged_sorted

def merge_with_paths(bd_df, path_df):
    
    merged = bd_df.merge(path_df, how="inner", on="Timestamp")
    merged_sorted = merged.sort_values("Timestamp")
    
    return merged_sorted

def all_bds(csvinpath, picklefile, flag, paths):
    
    flag_df = clean_tstamps(pd.read_csv(flag))
    path_df = clean_tstamps(pd.read_csv(paths))
    bd_df = filter_to_bd(csvinpath, picklefile)
    
    return merge_with_paths(merge_with_flags(bd_df, flag_df), path_df)

def filt_struct_bds(bd_df):
    
    #From XBOX3 expert Ben Woolley pg 145
    mask = (bd_df["BD_PSR_amp"] & bd_df["BD_PERA"] & (~bd_df["BD_PERA"]))
    struct_bds = bd_df[mask]
    
    struct_bds.sort_values("Timestamp", inplace=True)
    struct_bds.reset_index(drop=True, inplace=True)
    
    return struct_bds
    
if __name__ == "__main__":
    cli_parser = argparse.ArgumentParser(description = 'Filter to breakdowns, by chosen dates')
    cli_parser.add_argument('-c', '--csvinpath', type=str, metavar='', required = True, 
                        help = 'Path of csv infile')
    cli_parser.add_argument('-p', '--picklefile', type=str, metavar='', required = True, 
                        help = 'path to segments pickle')
    cli_parser.add_argument('-o', '--csvoutpath', type=str, metavar='', required = True, 
                        help = 'Name of output file after filtering, for the event data')
    cli_parser.add_argument('-f', '--flag', type=str, metavar='', required = True, 
                        help = 'Location of df containing flag variables')
    cli_parser.add_argument('-l', '--paths', type=str, metavar='', required = True, 
                        help = 'Location of df containing path variables, for memoisation')
    args = cli_parser.parse_args()
