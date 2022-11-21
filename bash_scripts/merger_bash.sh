#!/bin/bash
HOME="/home/student.unimelb.edu.au/pushkarnap/Documents/xbox_scripts/masters_code_27062022"
CSVLOC="/scraped_data"
DSET="/xbox3_td24ubol4_data/missing_energy"
INPATH="${HOME}${CSVLOC}${DSET}"
KNAME="Timestamp"

OUTPATH="${HOME}${CSVLOC}${DSET}/xbox3_td24ubol4_full.parq"
echo "Now merging ${DSET}"
python merge_csvs.py -f $INPATH -o $OUTPATH -k $KNAME
echo "Merged ${DSET}"
