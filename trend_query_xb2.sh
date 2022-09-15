#!/bin/bash

HDF_PATH="/media/pushkarnap/Expansion/xbox2_td24_2018/hdf/trend"

OCSV_PATH="/home/student.unimelb.edu.au/pushkarnap/Documents/xbox_scripts/masters_code_27062022/scraped_data/xbox2_td24trend_data"

# python scrape_trend.py -f $HDF_PATH -c "${OCSV_PATH}/xbox3_td24_dut1pc.csv" \
# -l 'Timestamp' -l 'DUT 1 Pressure'
# python scrape_trend.py -f $HDF_PATH -c "${OCSV_PATH}/xbox3_td24_dut1pg.csv" \
# -l 'Timestamp' -l 'Gauge DUT 1 Pressure '
# python scrape_trend.py -f $HDF_PATH -c "${OCSV_PATH}/xbox3_td24_dut2pc.csv" \
# -l 'Timestamp' -l 'DUT2 Pressure'
# python scrape_trend.py -f $HDF_PATH -c "${OCSV_PATH}/xbox3_td24_dut2pg.csv" \
# -l 'Timestamp' -l 'Gauge DUT 2 Pressure '
python scrape_trend_xb2.py -f $HDF_PATH -c "${OCSV_PATH}/xbox2_td24_ip_lwin.csv" \
-l "Timestamp" -l "Loadside win"
echo '''python scrape_trend.py -f $HDF_PATH -c "${OCSV_PATH}/xbox2_td24_ip_lwin.csv" \
-l "Timestamp" -l "Loadside win"'''
# python scrape_trend_xb2.py -f $HDF_PATH -c "${OCSV_PATH}/xbox2_td24_ip_prepc.csv" \
# -l "Timestamp" -l "IP before PC"
# echo '''python scrape_trend.py -f $HDF_PATH -c "${OCSV_PATH}/xbox2_td24_ip_prepc.csv" \
# -l "Timestamp" -l "IP before PC"'''
# python scrape_trend_xb2.py -f $HDF_PATH -c "${OCSV_PATH}/xbox2_td24_ip_pc.csv" \
# -l 'Timestamp' -l 'PC IP'
# echo '''python scrape_trend.py -f $HDF_PATH -c "${OCSV_PATH}/xbox2_td24_ip_pc.csv" \
# -l "Timestamp" -l "PC IP"'''


