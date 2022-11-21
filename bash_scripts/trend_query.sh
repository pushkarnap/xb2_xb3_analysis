#!/bin/bash

HDF_PATH="/media/pushkarnap/Expansion/xbox3_td24_20182020/hdf/trend"

OCSV_PATH="/home/student.unimelb.edu.au/pushkarnap/Documents/xbox_scripts/masters_code_27062022/scraped_data/xbox3_td24trend_data"

# python scrape_trend.py -f $HDF_PATH -c "${OCSV_PATH}/xbox3_td24_dut1pc.csv" \
# -l 'Timestamp' -l 'DUT 1 Pressure'
# python scrape_trend.py -f $HDF_PATH -c "${OCSV_PATH}/xbox3_td24_dut1pg.csv" \
# -l 'Timestamp' -l 'Gauge DUT 1 Pressure '
# python scrape_trend.py -f $HDF_PATH -c "${OCSV_PATH}/xbox3_td24_dut2pc.csv" \
# -l 'Timestamp' -l 'DUT2 Pressure'
# python scrape_trend.py -f $HDF_PATH -c "${OCSV_PATH}/xbox3_td24_dut2pg.csv" \
# -l 'Timestamp' -l 'Gauge DUT 2 Pressure '
python scrape_trend.py -f $HDF_PATH -c "${OCSV_PATH}/xbox3_td24_pulscomp1p.csv" \
-l 'Timestamp' -l 'Pulse Compressor 1 Pressure'
python scrape_trend.py -f $HDF_PATH -c "${OCSV_PATH}/xbox3_td24_pulscomp2p.csv" \
-l 'Timestamp' -l 'Pulse Compressor 2 Pressure'


