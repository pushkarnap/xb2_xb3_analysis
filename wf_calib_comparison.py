import argparse 
import h5py
import numpy as np
import matplotlib.pyplot as plt
from dateutil import parser
import time
from wf_retriever import plot_wf, scale_yaxis

if __name__ == '__main__':
    cli_parser = argparse.ArgumentParser(description = 'Plot event data waveforms')
    cli_parser.add_argument('-f', '--filepath', type=str, metavar='', required = True, 
                        help = 'HDF filepath')
    cli_parser.add_argument('-p', '--pulse', type=str, metavar='', required = True, 
                        help = 'Name of pulse')
    args = cli_parser.parse_args()
