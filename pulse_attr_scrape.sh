#!/bin/bash
HDF_PATH="/media/pushkarnap/Expansion/xbox3_td24_20182020/hdf/a_bo_l3"
echo $HDF_PATH
CSV_NAME="xbox3_td24_a_bo_l3_bd_struct_flags.csv"
echo $CSV_NAME
echo "python query_pulse.py -f ${HDF_PATH} -c ${CSV_NAME} \
-l Timestamp -l Pulse Count -l Log Type -l Line"
python query_pulse.py -f $HDF_PATH -c $CSV_NAME \
-l "Timestamp" -l "BD_DC_UP" -l "BD_DC_DOWN"

