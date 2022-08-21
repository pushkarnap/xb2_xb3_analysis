#!/bin/bash
HDF_PATH="/media/pushkarnap/Expansion/xbox3_td24_20182020/hdf/trend"
echo $HDF_PATH
CSV_NAME="xbox3_td24_trend_pressure.csv"
echo $CSV_NAME
echo "python scrape_trend.py -f ${HDF_PATH} -c ${CSV_NAME} -p trend_files.pickle \
-l Timestamp -l DUT 1 Pressure -l Gauge DUT 1 Pressure"
python scrape_trend.py -f $HDF_PATH -c $CSV_NAME -p trend_files.pickle \
-l 'Timestamp' -l 'DUT 1 Pressure' -l 'Gauge DUT 1 Pressure '

