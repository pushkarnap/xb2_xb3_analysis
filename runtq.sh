#!/bin/bash

#initial data paths for xb3 data
DATA_PATH="/media/pushkarnap/Expansion/xbox3_td24_20182020/hdf"
L3_PATH="${DATA_PATH}/a_bo_l3"
L4_PATH="${DATA_PATH}/b_ubo_l4"
TREND_PATH="${DATA_PATH}/trend"

#initial scraped data paths for xb3 data
L3_CSV="/home/student.unimelb.edu.au/pushkarnap/Documents/xbox_scripts/masters_code_27062022/scraped_data/xbox3_td24bol3_data"
L4_CSV="/home/student.unimelb.edu.au/pushkarnap/Documents/xbox_scripts/masters_code_27062022/scraped_data/xbox3_td24ubol4_data"
TR_CSV="/home/student.unimelb.edu.au/pushkarnap/Documents/xbox_scripts/masters_code_27062022/scraped_data/xbox3_td24trend_data"

# echo "Filtering for breakdowns"
# 
# python bd_filt.py \
# -i "${L3_CSV}/xbox3_td24bol3_psi.csv" \
# -p "${L3_CSV}/xbox3_td24bol3_segp.pickle" \
# -f "${L3_CSV}/xbox3_td24bol3_flag.csv" \
# -m "${L3_CSV}/xbox3_td24bol3_path.csv" \
# -t "${L3_CSV}/xbox3_td24bol3_tquery_pc.csv" \
# -o "${L3_CSV}/xbox3_td24bol3_pc1bd.csv" \
# -c "PSI_amp max (scaled)"

# echo "Done filtration of bds, query constructed"
# echo "Querying trend data"
# 
python syncing.py \
-i "${L4_CSV}/queries/xbox3_td24ubol4_tquery_pc.csv" \
-t "${TR_CSV}/xbox3_td24_dut2pc.csv" \
-o "${L4_CSV}/query_results/xbox3_td24ubol4_tquery_pcbd_dut2p.csv" \
-x 0
# python syncing.py \
# -i "${L4_CSV}/xbox3_td24ubol4_tquery_pc.csv" \
# -t "${TR_CSV}/xbox3_td24_pulscomp2p.csv" \
# -o "${L4_CSV}/xbox3_td24ubol4_tquery_pc_result.csv" \
# -x 0
# echo "Done querying trend data"

# echo "Filtering for breakdowns"
# 
# python bd_filt.py \
# -i "${L4_CSV}/xbox3_td24ubol4_psi.csv" \
# -p "${L4_CSV}/xbox3_td24ubol4_segp.pickle" \
# -f "${L4_CSV}/xbox3_td24ubol4_flag.csv" \
# -m "${L4_CSV}/xbox3_td24ubol4_path.csv" \
# -t "${L4_CSV}/xbox3_td24ubol4_tquery_pc.csv" \
# -o "${L4_CSV}/xbox3_td24ubol4_pc2bd.csv" \
# -c "PSI_amp max (scaled)"
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
