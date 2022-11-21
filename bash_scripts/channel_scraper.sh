#!/bin/bash
DATA_PATH="/media/pushkarnap/Expansion"
XB2="/xbox2_td24_2018"
XB3="/xbox3_td24_20182020"
IN_PATH="${DATA_PATH}${XB3}/hdf/a_bo_l3"

STORE_PATH="/home/student.unimelb.edu.au/pushkarnap/Documents/xbox_scripts/masters_code_27062022/scraped_data"
DSET="/xbox3_td24bol3_data"
CALC="/missing_energy"
OUT_PATH_INC="${STORE_PATH}${DSET}${CALC}/vs_spartan.csv"
# OUT_PATH_TRA="${STORE_PATH}${DSET}${CALC}/xbox3_td24bol3_U_TRA.csv"
# OUT_PATH_REF="${STORE_PATH}${DSET}${CALC}/xbox3_td24bol3_U_REF.csv"
# OUT_PATH_PW="${STORE_PATH}${DSET}${CALC}/xbox3_td24bol3_pw.csv"
# OUT_PATH_AMP="${STORE_PATH}${DSET}${CALC}/xbox3_td24bol3_amp.csv"

echo "start l3 xb3"
python scrape_channel.py -f $IN_PATH -c $OUT_PATH_INC -p "PSI_amp" -s "get_pulse_energy" -n "U_INC"
# python scrape_channel.py -f $IN_PATH -c $OUT_PATH_TRA -p "PEI_amp" -s "get_pulse_energy" -n "U_TRA"
# python scrape_channel.py -f $IN_PATH -c $OUT_PATH_REF -p "PSR_amp" -s "get_pulse_energy" -n "U_REF"
# python scrape_channel.py -f $IN_PATH -c $OUT_PATH_PW -p "PSI_amp" -s "get_pulse_width" -n "INC_PulseWidth"
# python scrape_channel.py -f $IN_PATH -c $OUT_PATH_AMP -p "PSI_amp" -s "get_pulse_meanamp" -n "INC_MeanAmp"
echo "end l3 xb3"
# 
# IN_PATH="${DATA_PATH}${XB3}/hdf/b_ubo_l4"
# DSET="/xbox3_td24ubol4_data"
# CALC="/missing_energy"
# OUT_PATH_INC="${STORE_PATH}${DSET}${CALC}/xbox3_td24ubol4_U_INC.csv"
# OUT_PATH_TRA="${STORE_PATH}${DSET}${CALC}/xbox3_td24ubol4_U_TRA.csv"
# OUT_PATH_REF="${STORE_PATH}${DSET}${CALC}/xbox3_td24ubol4_U_REF.csv"
# OUT_PATH_PW="${STORE_PATH}${DSET}${CALC}/xbox3_td24ubol4_pw.csv"
# OUT_PATH_AMP="${STORE_PATH}${DSET}${CALC}/xbox3_td24ubol4_amp.csv"
# 
# echo "start l4 xb3"
# python scrape_channel.py -f $IN_PATH -c $OUT_PATH_INC -p "PSI_amp" -s "get_pulse_energy" -n "U_INC"
# python scrape_channel.py -f $IN_PATH -c $OUT_PATH_TRA -p "PEI_amp" -s "get_pulse_energy" -n "U_TRA"
# python scrape_channel.py -f $IN_PATH -c $OUT_PATH_REF -p "PSR_amp" -s "get_pulse_energy" -n "U_REF"
# python scrape_channel.py -f $IN_PATH -c $OUT_PATH_PW -p "PSI_amp" -s "get_pulse_width" -n "INC_PulseWidth"
# python scrape_channel.py -f $IN_PATH -c $OUT_PATH_AMP -p "PSI_amp" -s "get_pulse_meanamp" -n "INC_MeanAmp"
# wait
# echo "end l4 xb3"
