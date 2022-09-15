import pandas as pd
import numpy as np

STD_SAMPLE = 25

def joiner(tstamps, pressure):
    
    tstamps_j = tstamps.reshape((1, len(tstamps)))
    pressure_j = pressure.reshape((1, len(pressure)))
    
    return np.concatenate((tstamps_j, pressure_j))

def padder(tstamps, pressure, topad):
    
    tstamps_n = np.pad(tstamps, (topad, 0), 'constant', constant_values = (np.nan, 0))
    pressure_n = np.pad(pressure, (topad, 0), 'constant', constant_values = (np.nan, 0))
    
    return tstamps_n, pressure_n
        
def create_plotting_matrix(p_df_csv, channel):
    
    p_df = pd.read_csv(p_df_csv, parse_dates=["TimestampDT", "TimestampBD"], index_col=0)
    p_df["TimestampRel"] = (p_df["TimestampDT"] - p_df["TimestampBD"]).to_numpy().astype("int64")/1e9
    groupedonbd = p_df.groupby("TimestampBD")
    
    matrix = []
    for name, group in groupedonbd:
        tstamps = np.array(group["TimestampRel"])
        pressure = np.array(group[channel])
        samples = group.shape[0]
        if samples < STD_SAMPLE:
            diff = STD_SAMPLE - samples
            matrix.append(joiner(*padder(tstamps, pressure, diff)))
        if samples > STD_SAMPLE:
            diff = samples - STD_SAMPLE
            matrix.append(joiner(tstamps[diff:], pressure[diff:]))
        if samples == STD_SAMPLE:
            matrix.append(joiner(tstamps, pressure))
        
    return np.array(matrix)

def pre_spike_pc(p_df_csv, channel, thresh):
    
    p_df = pd.read_csv(p_df_csv, parse_dates=["TimestampDT", "TimestampBD"], index_col=0)
    p_df["TimestampRel"] = (p_df["TimestampDT"] - p_df["TimestampBD"]).to_numpy().astype("int64")/1e9
    groupedonbd = p_df.groupby("TimestampBD")
    
    def det_spike_wrap(df):
    
        def det_spike(df, channel, thresh):
            press = np.array(df[channel])
            t = np.array(df["TimestampRel"])
            ratio = np.pad(press[1:]/press[:-1], (1,0), 'constant', constant_values=(0,0))
            spike_locs = np.nonzero(ratio > thresh)
            spike_times = t[spike_locs]
            if spike_times.size > 0:
                main_spike_loc = np.argmin(np.abs(spike_times))
                return spike_times[main_spike_loc]
            else:
                return np.nan
    
        return det_spike(df, channel, thresh)
    
    main_spike_time = groupedonbd.apply(det_spike_wrap)
    pre_bd = len(main_spike_time[main_spike_time < 0])
    pc = (pre_bd/len(main_spike_time))*100
    
    return pc, main_spike_time

def nan_finder(p_df_csv, channel):
    #find the occurence of nans relative to the waveform breakdown time.
    p_df = pd.read_csv(p_df_csv, parse_dates=["TimestampDT", "TimestampBD"], index_col=0)
    p_df["TimestampRel"] = (p_df["TimestampDT"] - p_df["TimestampBD"]).to_numpy().astype("int64")/1e9
    groupedonbd = p_df.groupby("TimestampBD")
    
    def det_nan_loc_wrap(df):
        
        def det_nan_loc(df, channel):
            press = np.array(df[channel])
            times = np.array(df["TimestampRel"])
            wherenan = np.isnan(press)
            nan_times = times[wherenan]
            min_nan = np.amin(nan_times)
            if min_nan > 0:
                return min_nan 
            else:
                return np.amax(nan_times)
        
        return det_nan_loc(df, channel)
    
    nan_reltime = groupedonbd.apply(det_nan_loc_wrap)
    
    return nan_reltime











