#!/bin/bash
INCSV_LOC="/home/student.unimelb.edu.au/pushkarnap/Documents/xbox_scripts/masters_code_27062022/scraped_data/xbox3_td24ubol4_data/xbox3_td24ubol4_pcBD_tq.csv"
OUTCSV_LOC="/home/student.unimelb.edu.au/pushkarnap/Documents/xbox_scripts/masters_code_27062022/scraped_data/xbox3_td24ubol4_data/xbox3_td24ubol4_pcBD_pulscomp2p.csv"
DATA_LOC="/home/student.unimelb.edu.au/pushkarnap/Documents/xbox_scripts/masters_code_27062022/scraped_data/xbox3_td24trend_data/xbox3_td24_pulscomp2p.csv"

echo $INCSV_LOC
echo $OUTCSV_LOC
echo $DATA_LOC
python syncing.py -i $INCSV_LOC -t $DATA_LOC -o $OUTCSV_LOC -x 0
