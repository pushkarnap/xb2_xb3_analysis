#!/bin/bash
HDF_PATH="/media/pushkarnap/Expansion/xbox3_td24_20182020/hdf/a_bo_l3"
echo $HDF_PATH
CSV_NAME="scraped_data/xbox3_td24_a_bo_l3_bd_struct_flags.csv"
echo $CSV_NAME
python query_pulse.py -f $HDF_PATH -c $CSV_NAME \
-l "Timestamp" -l "BD_DC_UP" -l "BD_DC_DOWN" -l "BD_PSR_amp" -l "BD_PLRA" -l "BD_PKRA" -l "BD_PERA"

