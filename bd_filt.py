import pandas as pd
import numpy as np
import datetime as dt
import argparse
from manual_selection import clean_tstamps, apply_pthresh, POWER_THRESH
from dateutil.relativedelta import relativedelta
import pickle

QSTART = 10
QEND = 10
BD_LOG = 2 #'2' for XBOX3, '3' for XBOX2

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

def filter_to_bd(csvinpath, picklefile, pchannel):
    df = pd.read_csv(csvinpath)
    df = clean_tstamps(df)
    df_pfilt = apply_pthresh(df, pchannel)
    
    segments = []
    with open(picklefile, "rb") as fhand:
        segments = pickle.load(fhand)
        
    df_pdfilt = filter_by_date(df_pfilt, segments)
    df_PowerDateBD_filt = df_pdfilt[df_pdfilt["Log Type"] == BD_LOG]
    
    return df_PowerDateBD_filt

def merge_with_flags(bd_df, flag_df):
    merged = bd_df.merge(flag_df, how="inner", on="Timestamp")
    merged_sorted = merged.sort_values("Timestamp")
    
    return merged_sorted

def merge_with_paths(bd_df, path_df):
    merged = bd_df.merge(path_df, how="inner", on="Timestamp")
    merged_sorted = merged.sort_values("Timestamp")
    
    return merged_sorted

def all_bds(csvinpath, picklefile, flag, paths, pchannel):
    flag_df = clean_tstamps(pd.read_csv(flag))
    path_df = clean_tstamps(pd.read_csv(paths))
    bd_df = filter_to_bd(csvinpath, picklefile, pchannel)
    
    return merge_with_paths(merge_with_flags(bd_df, flag_df), path_df)

def filt_struct_bds(bd_df):
    #From XBOX3 expert Ben Woolley pg 145
    #PLRA channel added on Matteo Volpi instruction
    #THIS FUNCTION MUST BE MANUALLY EDITED BEFORE EACH EXECUTION
    #Different combinations determine the breakdowns being considered
    
    #XBOX2 Config structure bds
    #struct_bds = bd_df[bd_df["BD_DC Up"] & (~bd_df["BD_PER log"]) \
            #& bd_df["BD_PKR log"] & bd_df["BD_PSR log"]]
    
    
    #XBOX3 Pulse compressor bd configs
    struct_bds = bd_df[bd_df["BD_PLRA"] & \
                        bd_df["BD_PKRA"] & \
                        (~bd_df["BD_PERA"]) & \
                        (~bd_df["BD_PSR_amp"]) & \
                        (~bd_df["BD_DC_UP"])]
    
    
    mask = (np.array(bd_df["BD_PLRB"]).astype('bool') & \
            np.array(bd_df["BD_PKRB"]).astype('bool') & \
            (~np.array(bd_df["BD_PERB"]).astype('bool')) & \
            (~np.array(bd_df["BD_PSR_amp"]).astype('bool')) & \
            (~np.array(bd_df["BD_DC_UP"]).astype('bool')))
    select_bds = bd_df[mask]
    
    return select_bds.sort_values("Timestamp").reset_index(drop=True)

def do_bd_filter(csvinpath, picklefile, flag, paths, pchannel):
    allbd_df = all_bds(csvinpath, picklefile, flag, paths, pchannel)
    selectbd_df = filt_struct_bds(allbd_df) 
    
    return selectbd_df

def create_trend_name(event_file_name):
    date = event_file_name.split("_")[1]
    trend_name = f"TrendData_{date}.hdf"
    
    return trend_name
    
def construct_trend_queries(structbd_df):
    qtrend_df = structbd_df.loc[:, ["Timestamp"]]
    qtrend_df.rename(columns = {"Timestamp": "TimestampBD"}, inplace=True)
                                #"FileName": "FileNameEvent"}, inplace=True)
    
    qtrend_df["StartTrendQ"] = qtrend_df["TimestampBD"]\
        .apply(lambda x: x - relativedelta(seconds = QSTART))
    qtrend_df["EndTrendQ"] = qtrend_df["TimestampBD"]\
        .apply(lambda x: x + relativedelta(seconds = QEND))
    #qtrend_df["FileNameTrend"] = qtrend_df["FileNameEvent"]\
        #.apply(create_trend_name)
    
    return qtrend_df

def write_trend_queries(csvinpath, picklefile, flag, 
                        paths, tquery, csvoutpath, pchannel):
    selectbd_df = do_bd_filter(csvinpath, picklefile, flag, paths, pchannel)
    selectbd_df.to_csv(csvoutpath)
    qtrend_df = construct_trend_queries(selectbd_df)
    qtrend_df.to_csv(tquery)
    
    return

if __name__ == "__main__":
    cli_parser = argparse.ArgumentParser(description = 'Construct query to retrieve trend data based on BDs extracted from conditioning plot.')
    
    cli_parser.add_argument('-i', '--csvinpath', type=str, metavar='', required = True, 
                        help = 'PSI conditioning input filepath')
    cli_parser.add_argument('-p', '--segpickle', type=str, metavar='', required = True, 
                        help = 'List of tuples containing beginning and end points of selected data')
    cli_parser.add_argument('-f', '--flagfile', type=str, metavar='', required = True, 
                        help = 'Scraped csvpath containing the BD flags')
    cli_parser.add_argument('-m', '--pathfile', type=str, metavar='', required = True, 
                        help = 'Scraped csvpath containing the memoisation info')
    cli_parser.add_argument('-t', '--tquery', type=str, metavar='', required = True, 
                        help = 'Outpath of csv for finalised trend query')
    cli_parser.add_argument('-o', '--csvoutpath', type=str, metavar='', required = True, 
                        help = 'Outpath of csv for selected bds')
    cli_parser.add_argument('-c', '--pchannel', type=str, metavar='', required = True, 
                        help = 'Name of channel to filter by power threshold')
    args = cli_parser.parse_args()
    
    write_trend_queries(args.csvinpath, args.segpickle, 
                        args.flagfile, args.pathfile, args.tquery,
                        args.csvoutpath, args.pchannel)
    
    
    
    
