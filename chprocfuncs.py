"""FUNCTIONS TO PROCESS CHANNELS IN TESTSTAND DATA"""
import numpy as np
import h5py
from scipy.integrate import trapezoid as trapz
import pandas as pd


def clean_tstamps(df):
    df["Timestamp"] = df["Timestamp"].astype("string").str.split("'").str[1]
    df["Timestamp"] = pd.to_datetime(df["Timestamp"],
                                     format="%Y-%m-%dT%H:%M:%S.%fZ",
                                     utc=True)

    return df


def scale_yaxis(yaxis, c0, c1, c2):
    '''
    Helper function for scaling application
    @param yaxis: np array of raw adc counts, as type float64
    @param c0: offset coefficient
    @param c1: linear coefficient
    @param c2: quadratic coefficient
    @return scaled np array of waveform
    '''
    scaled = c2 * (np.square(yaxis)) + c1 * yaxis + c0
    return scaled


def scale_pow(wf):
    '''
    Apply scaling to raw ADC counts
    @param wf: HDF dataset object of candidate waveform
    @return scaled np array of dataset
    '''
    c0 = wf.attrs.get("Scale_Coeff_c0", 0)
    c1 = wf.attrs.get("Scale_Coeff_c1", 1)
    c2 = wf.attrs.get("Scale_Coeff_c2", 0)
    scaled_wf = scale_yaxis(wf[:].astype('float64'), c0, c1, c2)
    return scaled_wf


def find_rise(adc, t):
    '''
    Given raw ADC counts, finds the rising edge of the waveform
    @param adc: Raw ADC counts of waveform being considered
    @param t: times associated with each sample of the waveform
    @returns rising edge time of the waveform
    '''
    step = np.hstack((np.ones(len(adc)), -1 * np.ones(len(adc))))
    adc_step = np.convolve(adc - np.mean(adc), step, mode="valid")[:-1]

    return t[np.argmax(adc_step)]


def find_fall_frac(adc, t, frac):
    '''
    Given raw ADC counts, finds the `frac' falling edge of the waveform
    @param adc: Raw ADC counts of waveform being considered
    @param t: times associated with each sample of the waveform
    @param frac: the 'frac' percent falling edge
    @returns frac percent falling edge time of the waveform
    '''
    signs = np.sign(adc - np.amax(adc) * frac)
    sign_change = (signs[:-1] != signs[1:])
    pret = t[np.r_[sign_change, [False]]]
    postt = t[np.r_[[False], sign_change]]
    interp = ((pret + postt) / 2)
    return interp


def get_pulse_energy(hdf_file, chname):
    '''
    Aggregation operation on ADC waveforms, integrate over waveform span.
    @param hdf_file: Path object of HDF file
    @param chname: name of channel to run aggregation over
    @return list of lists (rows) of timestamp and aggregated qty
    '''
    drows = []

    try:
        hdf_fhand = h5py.File(hdf_file, "r")
    except:
        print(f"Could not open file {hdf_file}")
        return []

    pulses = list(hdf_fhand.keys())
    for pulse in pulses:

        wf = hdf_fhand[pulse][chname]
        tstamp = hdf_fhand[pulse].attrs.get("Timestamp", np.nan)
        samples = wf.attrs.get("wf_samples", 0)

        inc = 0
        samples_arr = []
        drow = []

        if samples and (samples == wf.shape[0]):
            inc = wf.attrs["wf_increment"]
            t = np.linspace(0, samples * inc, samples)
            drow = [tstamp, trapz(scale_pow(wf), t)]
            drows.append(drow)

        else:
            drow = [tstamp, np.nan]
            drows.append(drow)

    hdf_fhand.close()
    return drows


def get_pulse_attr(hdf_file, chname):
    '''
    Retrieve pulse attr (Log Type, all BD flags) for each pulse. 
    @param chname: BD flag to scrape
    @param hdf_file: chosen hdf file
    @return list of lists (rows) of tstamp and attr
    '''
    drows = []

    try:
        hdf_fhand = h5py.File(hdf_file, "r")
    except:
        print(f"Could not open file {hdf_file}")
        return []

    pulses = list(hdf_fhand.keys())
    for pulse in pulses:
        tstamp = hdf_fhand[pulse].attrs.get("Timestamp", np.nan)
        attr = hdf_fhand[pulse].attrs.get(chname, np.nan)
        drow = [tstamp, attr]
        drows.append(drow)

    hdf_fhand.close()
    return drows


def get_pulse_width(hdf_file, chname):
    '''
    Find pulse width for each pulse in file.
    @param chname: BD flag to scrape
    @param hdf_file: chosen hdf file
    @return list of lists (rows) of tstamp and pulse width
    '''
    drows = []

    try:
        hdf_fhand = h5py.File(hdf_file, "r")
    except:
        print(f"Could not open file {hdf_file}")
        return []

    pulses = list(hdf_fhand.keys())
    for pulse in pulses:
        tstamp = hdf_fhand[pulse].attrs.get("Timestamp", np.nan)
        wf = hdf_fhand[pulse][chname]
        samples = wf.attrs.get("wf_samples", 0)

        inc = 0
        samples_arr = []
        drow = []

        if samples and (samples == wf.shape[0]):
            inc = wf.attrs["wf_increment"]
            t = np.linspace(0, samples * inc, samples)
            adc = wf[:].astype('float64')
            cut = find_fall_frac(adc, t, 0.9)
            t_f = np.amax(cut)
            t_r = np.amin(cut)
            pw = np.abs(t_f - t_r)
            drow = [tstamp, pw]
            drows.append(drow)

        else:
            drow = [tstamp, np.nan]
            drows.append(drow)

    hdf_fhand.close()
    return drows


def get_pulse_meanamp(hdf_file, chname):
    '''
    Integrate raw ADC counts over the pulse length, scale, and return
    @param chname: BD flag to scrape
    @param hdf_file: chosen hdf file
    @returns scaled pulse amplitude in watts
    '''
    drows = []

    try:
        hdf_fhand = h5py.File(hdf_file, "r")
    except:
        print(f"Could not open file {hdf_file}")
        return []

    pulses = list(hdf_fhand.keys())
    for pulse in pulses:
        tstamp = hdf_fhand[pulse].attrs.get("Timestamp", np.nan)
        wf = hdf_fhand[pulse][chname]
        samples = wf.attrs.get("wf_samples", 0)

        inc = 0
        samples_arr = []
        drow = []
        if samples and (samples == wf.shape[0]):
            inc = wf.attrs["wf_increment"]
            t = np.linspace(0, samples * inc, samples)
            adc = wf[:].astype('float64')
            cut = find_fall_frac(adc, t, 0.9)
            t_f = np.amax(cut)
            t_r = np.amin(cut)
            pw = np.abs(t_f - t_r)
            # scaled_wf = scaled_pow(wf)

            mask = (t >= t_r) & (t <= t_f)
            adc_filt = adc[mask]
            t_filt = t[mask]
            mean_amp_adc = trapz(adc_filt, t_filt) / pw
            mean_amp_watt = scale_yaxis(mean_amp_adc,
                                        wf.attrs.get("Scale_Coeff_c0", 0),
                                        wf.attrs.get("Scale_Coeff_c1", 1),
                                        wf.attrs.get("Scale_Coeff_c2", 0))
            drow = [tstamp, mean_amp_watt]
            drows.append(drow)

        else:
            drow = [tstamp, np.nan]
            drows.append(drow)

    hdf_fhand.close()
    return drows


def get_pulse_max(hdf_file, chname):
    '''
    Given raw ADC counts, finds the maximum of the waveform in watts
    @param hdf_file: Path object of HDF file
    @param chname: name of channel to run aggregation over
    @return list of lists (rows) of timestamp and aggregated qty
    '''
    drows = []

    try:
        hdf_fhand = h5py.File(hdf_file, "r")
    except:
        print(f"Could not open file {hdf_file}")
        return []

    pulses = list(hdf_fhand.keys())
    for pulse in pulses:

        wf = hdf_fhand[pulse][chname]
        tstamp = hdf_fhand[pulse].attrs.get("Timestamp", np.nan)
        samples = wf.attrs.get("wf_samples", 0)

        inc = 0
        samples_arr = []
        drow = []

        if samples and (samples == wf.shape[0]):
            adc_max = np.amax(wf[:].astype("float64"))
            maximum = scale_yaxis(adc_max,
                                  wf.attrs.get("Scale_Coeff_c0", 0),
                                  wf.attrs.get("Scale_Coeff_c1", 1),
                                  wf.attrs.get("Scale_Coeff_c2", 0))
            drow = [tstamp, maximum]
            drows.append(drow)

        else:
            drow = [tstamp, np.nan]
            drows.append(drow)

    hdf_fhand.close()
    return drows


chprocdispatcher = {"get_pulse_energy": get_pulse_energy,
                    "get_pulse_attr": get_pulse_attr,
                    "get_pulse_width": get_pulse_width,
                    "get_pulse_meanamp": get_pulse_meanamp,
                    "get_pulse_max": get_pulse_max}
