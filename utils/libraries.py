import os
import warnings
import numpy as np
import pandas as pd
from collections import deque
from scipy.signal import argrelextrema
from sklearn.linear_model import LinearRegression

from ta.volatility import BollingerBands
from ta.volume import OnBalanceVolumeIndicator, MFIIndicator
from ta.momentum import RSIIndicator, StochRSIIndicator, StochasticOscillator
from ta.trend import SMAIndicator, PSARIndicator, IchimokuIndicator, MACD, CCIIndicator

warnings.filterwarnings('ignore')