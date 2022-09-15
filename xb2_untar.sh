#!/bin/bash
TREND_DIR="/media/pushkarnap/Expansion/xbox2_td24_2018/tdms"

for entry in "$TREND_DIR"/*
do
tar -xvf $entry -C $TREND_DIR
done
