#!/bin/bash
USER="pushkarnap@spartan.hpc.unimelb.edu.au"
SPARTAN_PATH="/data/gpfs/projects/punim1158/pushkarnap"
LOCAL_PATH="/media/pushkarnap/Expansion"
FULL_REMOTE_PATH="${USER}:${SPARTAN_PATH}"

# scp -r "${LOCAL_PATH}/xbox2_td24_2018/hdf" $FULL_REMOTE_PATH
# scp -r "${LOCAL_PATH}/xbox3_td24_20182020/hdf" $FULL_REMOTE_PATH
scp chprocfuncs.py "$FULL_REMOTE_PATH/scraping_code"
