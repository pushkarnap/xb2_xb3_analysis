import pandas as pd
import datetime as dt
import numpy as np
import csv
import argparse

pd.options.mode.chained_assignment = None

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def lv_to_dt(df):
    
    lv_epoch = dt.datetime(year=1904, month=1, day=1, 
                           minute=0, second=0, microsecond=0, tzinfo=dt.timezone.utc)
    unix_epoch = dt.datetime(year=1970, month=1, day=1, 
                             minute=0, second=0, microsecond=0, tzinfo=dt.timezone.utc)
    lv_offset = (unix_epoch - lv_epoch).total_seconds()
    df["TimestampDT"] = pd.to_datetime(df["Timestamp"] - lv_offset , unit="s", utc=True)
    
    return df

def synchronise(query_df, feature_df, tq_outfile):
    
    query_results = []
    num_queries = query_df.shape[0]
    for i in range(num_queries):
        
        query = query_df.loc[i, ["StartTrendQ", "EndTrendQ", "TimestampBD"]]
        formed_query = (feature_df["TimestampDT"] >= query["StartTrendQ"]) & \
        (feature_df["TimestampDT"] <= query["EndTrendQ"])
        result_df = feature_df.loc[formed_query]
        bd_tstamps = np.repeat(query["TimestampBD"], result_df.shape[0])
        result_df["TimestampBD"] = bd_tstamps
        query_results.append(result_df)
        printProgressBar(i, num_queries)
        
    pd.concat(query_results).to_csv(tq_outfile)
    
    return

def run_trend_query(csvinpath, csvoutpath, trendpath, isxb2):
    
    print("reading trend data")
    if isxb2:
        feature_df = pd.read_csv(trendpath, parse_dates=["Timestamp"])
        feature_df.rename(columns = {"Timestamp": "TimestampDT"}, inplace=True)
    else:
        feature_df = lv_to_dt(pd.read_csv(trendpath))
    print("done loading trend data")
    query_df = pd.read_csv(csvinpath,
                   parse_dates=["TimestampBD", "StartTrendQ", "EndTrendQ"])
    synchronise(query_df, feature_df, csvoutpath)
    
    return

if __name__ == "__main__":
    
    cli_parser = argparse.ArgumentParser(description = 'Construct query to retrieve trend data based on BDs extracted from conditioning plot.')
    
    cli_parser.add_argument('-i', '--csvinpath', type=str, metavar='', required = True, 
                        help = 'Trend query earlier constructed')
    cli_parser.add_argument('-t', '--trendpath', type=str, metavar='', required = True, 
                        help = 'Trend data to query')
    cli_parser.add_argument('-o', '--csvoutpath', type=str, metavar='', required = True, 
                        help = 'Results of the trend data query for later manipulation.')
    cli_parser.add_argument('-x', '--isxb2', type=int, metavar='', required = True, 
                        help = '0 for no, 1 for yes (whether or not we are analysing xb2 data).')
    args = cli_parser.parse_args()
    
    run_trend_query(args.csvinpath, args.csvoutpath, args.trendpath, args.isxb2)
