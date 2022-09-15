#!/bin/bash
# initial paths for xbox2 data
DATA_PATH="/media/pushkarnap/Expansion/xbox2_td24_2018/hdf"
EVENT_PATH="${DATA_PATH}/event"
TREND_PATH="${DATA_PATH}/trend"

#initial scraped data paths for xb2 data
EVENT_CSV="/home/student.unimelb.edu.au/pushkarnap/Documents/xbox_scripts/masters_code_27062022/scraped_data/xbox2_td24event_data"
TREND_CSV="/home/student.unimelb.edu.au/pushkarnap/Documents/xbox_scripts/masters_code_27062022/scraped_data/xbox2_td24trend_data"

python syncing.py \
-i "${EVENT_CSV}/xbox2_td24_tquery.csv" \
-t "${TREND_CSV}/xbox2_td24_ip_prestruct.csv" \
-o "${EVENT_CSV}/xbox2_td24_tquery_prestruct.csv" \
-x 1 #is xbox2 or not, in this case yes, so -x 1

# echo "Filtering for breakdowns"
# 
# python bd_filt.py \
# -i "${EVENT_CSV}/xbox2_td24_psi.csv" \
# -p "${EVENT_CSV}/xbox2_td24_segp.pickle" \
# -f "${EVENT_CSV}/xbox2_td24_flag.csv" \
# -m "${EVENT_CSV}/xbox2_td24_path.csv" \
# -t "${EVENT_CSV}/xbox2_td24_tquery.csv" \
# -o "${EVENT_CSV}/xbox2_td24_structbd.csv" \
# -c "PSI Amplitude max (scaled)"
# 
# echo '''python bd_filt.py \
# -i "${EVENT_CSV}/xbox2_td24_psi.csv" \
# -p "${EVENT_CSV}/xbox2_td24_segp.pickle" \
# -f "${EVENT_CSV}/xbox2_td24_flag.csv" \
# -m "${EVENT_CSV}/xbox2_td24_path.csv" \
# -t "${EVENT_CSV}/xbox2_td24_tquery.csv" \
# -o "${EVENT_CSV}/xbox2_td24_structbd.csv" \
# -c "PSI Amplitude max (scaled)"'''
# echo "Filtering for breakdowns"
# 
# python bd_filt.py \
# -i "${L3_CSV}/xbox3_td24bol3_psi.csv" \
# -p "${L3_CSV}/xbox3_td24bol3_segp.pickle" \
# -f "${L3_CSV}/xbox3_td24bol3_flag.csv" \
# -m "${L3_CSV}/xbox3_td24bol3_path.csv" \
# -t "${L3_CSV}/xbox3_td24bol3_tquery.csv" \
# -o "${L3_CSV}/xbox3_td24bol3_structbd.csv"
# 
# echo "Done filtration of bds, query constructed"
# echo "Querying trend data"
# 
# python syncing.py \
# -i "${L3_CSV}/xbox3_td24bol3_tquery.csv" \
# -t "${TR_CSV}/xbox3_td24_dut1pc.csv" \
# -o "${L3_CSV}/xbox3_td24bol3_tquery_control.csv" \
# 
# python syncing.py \
# -i "${L4_CSV}/xbox3_td24ubol4_tquery.csv" \
# -t "${TR_CSV}/xbox3_td24_dut2pc.csv" \
# -o "${L4_CSV}/xbox3_td24ubol4_tquery_control.csv" \
# 
# echo "Done querying trend data"
# 
# echo "Filtering for breakdowns"
# 
# python bd_filt.py \
# -i "${L4_CSV}/xbox3_td24ubol4_psi.csv" \
# -p "${L4_CSV}/xbox3_td24ubol4_segp.pickle" \
# -f "${L4_CSV}/xbox3_td24ubol4_flag.csv" \
# -m "${L4_CSV}/xbox3_td24ubol4_path.csv" \
# -t "${L4_CSV}/xbox3_td24ubol4_tquery.csv" \
# -o "${L4_CSV}/xbox3_td24ubol4_structbd.csv"
# 
# echo "Done filtration of bds, query constructed"
# echo "Querying trend data"
# 
# python syncing.py \
# -i "${L4_CSV}/xbox3_td24ubol4_tquery.csv" \
# -t $TREND_PATH \
# -o "${L4_CSV}/xbox3_td24ubol4_tquery_result.csv" \
# -c "Gauge DUT 2 Pressure "
# 
# echo "Done querying trend data"
