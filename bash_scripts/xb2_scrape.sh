#!/bin/bash

#initial data paths for xb3 data
DATA_PATH="/media/pushkarnap/Expansion/xbox2_td24_2018/hdf"
IN_PATH="${DATA_PATH}/event"
OUT_PATH="scraped_data/xbox2_td24event_data"
OUT_CSV="${OUT_PATH}/xbox2_td24_path.csv"

# commands
python query_path.py -f $IN_PATH -c $OUT_CSV 

# outpaths for csv files, to store scraped data
# OUTCSV_BO="scraped_data/xbox3_td24bol3_psi.csv"
# OUTCSV_BO_FLAG="scraped_data/xbox3_td24bol3_flag.csv"
# OUTCSV_BO_PATH="scraped_data/xbox3_td24bol3_path.csv"
# 
# OUTCSV_UBO="scraped_data/xbox3_td24ubol4_psi.csv"
# OUTCSV_UBO_FLAG="scraped_data/xbox3_td24ubol4_flag.csv"
# OUTCSV_UBO_PATH="scraped_data/xbox3_td24ubol4_path.csv"
# 
# commands
# python condtn_event.py -f $E_PATH -c $OUTCSV_BO
# python query_pulse.py -f $L3_PATH -c $OUTCSV_BO_FLAG \
# -l "Timestamp" -l "BD_DC_UP" -l "BD_DC_DOWN" -l "BD_PSR_amp" -l "BD_PLRA" -l "BD_PKRA" -l "BD_PERA"
# python query_path.py -f $L3_PATH -c $OUTCSV_BO_PATH
# 
# python condtn_event.py -f $L4_PATH -c $OUTCSV_UBO
# python query_pulse.py -f $L4_PATH -c $OUTCSV_UBO_FLAG \
# -l "Timestamp" -l "BD_DC_UP" -l "BD_DC_DOWN" -l "BD_PSR_amp" -l "BD_PLRB" -l "BD_PKRB" -l "BD_PERB"
# python query_path.py -f $L4_PATH -c $OUTCSV_UBO_PATH
