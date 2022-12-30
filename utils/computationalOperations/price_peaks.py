from utils.libraries import *

def get_lows(vals, order = 5):
    low_idx = argrelextrema(vals, np.less, order = order)[0]
    return vals[low_idx]

def get_highs(vals, order = 5):
    high_idx = argrelextrema(vals, np.greater, order = order)[0]
    return vals[high_idx]

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]