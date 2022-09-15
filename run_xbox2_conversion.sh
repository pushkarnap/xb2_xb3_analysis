#!/bin/bash
DIR="/media/pushkarnap/Expansion/xbox2_td24_2018"
FILE_DIR="/home/student.unimelb.edu.au/pushkarnap/Documents/research_23062022_nodata/rfstudies/src"
SRC_DIR_TREND="${DIR}/tdms/trend"
SRC_DIR_EVENT="${DIR}/tdms/event/unconverted"

DEST_DIR_TREND="${DIR}/hdf/trend"
DEST_DIR_EVENT="${DIR}/hdf/event"

cd $FILE_DIR
# python transformation.py -v -s $SRC_DIR_TREND -d $DEST_DIR_TREND |& tee "${DIR}_trendconvlog.txt"
python transformation.py -v -s $SRC_DIR_EVENT -d $DEST_DIR_EVENT |& tee "${DIR}_eventconvlog.txt"
