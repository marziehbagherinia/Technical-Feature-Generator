from utils.config import *
from utils.libraries import *
from utils.computationalOperations.divergence import *
from utils.computationalOperations.price_peaks import *
from utils.computationalOperations.cross_lines import *
from utils.computationalOperations.linear_regression import *
from utils.computationalOperations.interval_position import *
from utils.computationalOperations.difference_from_line import *
from utils.computationalOperations.difference_from_value import *

class FeatureGenerator:

    def __init__(self, data):
        self.data = data

    def generate(self):
        self.rsi()
        self.stochRsi()
        self.stoch()
        self.sma()
        self.pSar()
        self.obv()
        self.mfi()
        self.bb()
        self.ichimoku()
        self.macd()
        self.cci()
        self.sr()
        self.divergence('rsi')
        self.divergence('stochRsi')
        self.divergence('stoch')
        self.divergence('obv')
        self.divergence('mfi')
        self.divergence('macd')
        self.divergence('cci')
        self.lch()
        
    def rsi(self):
        print("\tRSI Indicator!")
        rsi_value = RSIIndicator(self.data[CLOSE_COLUMN], fillna = True).rsi()
        
        rsi_over_80 = over_value(rsi_value, value = 80)
        rsi_under_20 = under_value(rsi_value, value = 20)

        self.data['rsi'] = rsi_value
        self.data['rsi_over_80'] = rsi_over_80
        self.data['rsi_under_20'] = rsi_under_20

    def stochRsi(self):
        print("\tStochastic RSI Indicator!")
        stochRsi = StochRSIIndicator(self.data[CLOSE_COLUMN], fillna = True)
        stochRsi_value = stochRsi.stochrsi()
        stochRsi_K = stochRsi.stochrsi_k()
        stochRsi_D = stochRsi.stochrsi_d()
        
        stochRsi_over_80 = over_value(stochRsi_value, value = 80/100)
        stochRsi_under_20 = under_value(stochRsi_value, value = 20/100)

        K_cross_D_bearish = cross_line_from_above(stochRsi_K, stochRsi_D)
        K_cross_D_bullish = cross_line_from_bottom(stochRsi_K, stochRsi_D)

        self.data['stochRsi'] = stochRsi_value
        self.data['stochRsi_K_value'] = stochRsi_K
        self.data['stochRsi_D_value'] = stochRsi_D
        self.data['stochRsi_over_80'] = stochRsi_over_80
        self.data['stochRsi_under_20'] = stochRsi_under_20
        self.data['stochRsi_K_cross_D_bearish'] = K_cross_D_bearish
        self.data['stochRsi_K_cross_D_bullish'] = K_cross_D_bullish

    def stoch(self):
        print("\tStochastic Indicator!")
        stoch = StochasticOscillator(self.data[HIGH_COLUMN], self.data[LOW_COLUMN], self.data[CLOSE_COLUMN], fillna = True)
        stoch_K = stoch.stoch()
        stoch_D = stoch.stoch_signal()
        
        stoch_over_80 = over_value(stoch_K, value = 80/100)
        stoch_under_20 = under_value(stoch_K, value = 20/100)

        K_cross_D_bearish = cross_line_from_above(stoch_K, stoch_D)
        K_cross_D_bullish = cross_line_from_bottom(stoch_K, stoch_D)

        #stoch_K_value = stoch (for calculating dicergence)
        self.data['stoch'] = stoch_K
        self.data['stoch_D_value'] = stoch_D
        self.data['stoch_over_80'] = stoch_over_80
        self.data['stoch_under_20'] = stoch_under_20
        self.data['stoch_K_cross_D_bearish'] = K_cross_D_bearish
        self.data['stoch_K_cross_D_bullish'] = K_cross_D_bullish

    def sma(self, length = 9):
        print("\tSImple MOving Average Indicator!")
        sma_value = SMAIndicator(self.data[CLOSE_COLUMN], length, fillna = True).sma_indicator()
        price_over_sma = over_line(self.data[CLOSE_COLUMN], sma_value)
        price_under_sma = under_line(self.data[CLOSE_COLUMN], sma_value)

        self.data[f'sma_{length}_value'.format(length = length)] = sma_value
        self.data[f'price_over_sma_{length}'.format(length = length)] = price_over_sma
        self.data[f'price_under_sma_{length}'.format(length = length)] = price_under_sma
    
    def pSar(self):
        print("\tSAR Indicator!")
        pSar_value = PSARIndicator(self.data[HIGH_COLUMN], self.data[LOW_COLUMN], self.data[CLOSE_COLUMN], fillna = True).psar()
        price_over_pSar = over_line(self.data[CLOSE_COLUMN], pSar_value)
        price_under_pSar = under_line(self.data[CLOSE_COLUMN], pSar_value)

        self.data['pSar_value'] = pSar_value
        self.data['price_over_pSar'] = price_over_pSar
        self.data['price_under_pSar'] = price_under_pSar

    def bb(self):
        print("\tBollinger Bands Indicator!")
        bb_value = BollingerBands(self.data[CLOSE_COLUMN], fillna=0)
        bb_upper_band = bb_value.bollinger_hband()
        bb_lowe_band = bb_value.bollinger_lband()

        bb_in_20_percent_of_band_top = top_of_interval(self.data[CLOSE_COLUMN], bb_upper_band, bb_lowe_band)
        bb_in_20_percent_of_band_bottom = bottom_of_interval(self.data[CLOSE_COLUMN], bb_upper_band, bb_lowe_band)

        price_cross_upper_band_bearish = cross_line_from_above(self.data[CLOSE_COLUMN], bb_upper_band)
        price_cross_lower_band_bullish = cross_line_from_bottom(self.data[CLOSE_COLUMN], bb_lowe_band)

        self.data['bb_upper_band'] = bb_upper_band
        self.data['bb_lowe_band'] = bb_lowe_band
        self.data['bb_in_20_percent_of_band_top'] = bb_in_20_percent_of_band_top
        self.data['bb_in_20_percent_of_band_bottom'] = bb_in_20_percent_of_band_bottom
        self.data['bb_price_cross_upper_band_bearish'] = price_cross_upper_band_bearish
        self.data['bb_price_cross_lower_band_bullish'] = price_cross_lower_band_bullish

    def obv(self):
        print("\tOBV Indicator!")
        obv_value = OnBalanceVolumeIndicator(self.data[CLOSE_COLUMN], self.data[VOLUME_COLUMN], fillna = 0).on_balance_volume()

        #TODO: Add other features for OBV indicator
        self.data['obv'] = obv_value

    def mfi(self):
        print("\tMFI Indicator!")
        mfi_value = MFIIndicator(self.data[HIGH_COLUMN], self.data[LOW_COLUMN], self.data[CLOSE_COLUMN], self.data[VOLUME_COLUMN], fillna = 0).money_flow_index()

        #TODO: Add other features for MFI indicator
        self.data['mfi'] = mfi_value

    def macd(self):
        print("\tMACD Indicator!")
        macd_indicator = MACD(self.data[CLOSE_COLUMN], fillna = 0)
        macd = macd_indicator.macd()
        signal = macd_indicator.macd_signal()

        self.data['macd'] = macd
        self.data['macd_signal'] = signal

    def cci(self):
        print("\tCCI Indicator!")
        cci_value = CCIIndicator(self.data[HIGH_COLUMN], self.data[LOW_COLUMN], self.data[CLOSE_COLUMN], fillna = 0).cci()

        self.data['cci'] = cci_value

    def ichimoku(self):
        print("\tIchimoku Indicator!")
        ichimoku_value = IchimokuIndicator(self.data[HIGH_COLUMN], self.data[LOW_COLUMN], fillna = True)
        span_a = ichimoku_value.ichimoku_a()
        span_b = ichimoku_value.ichimoku_b()        
        kijun_sen = ichimoku_value.ichimoku_base_line()
        tenkan_sen = ichimoku_value.ichimoku_conversion_line()
        
        tenkan_over_kijun = over_line(tenkan_sen, kijun_sen) #for long position
        spanaA_over_spanB = over_line(span_b, span_a) #for long position

        price_in_cloud_pos = interval_position(self.data[CLOSE_COLUMN], span_a, span_b)
        price_in_tenkan_and_kijun_pos = interval_position(self.data[CLOSE_COLUMN], tenkan_sen, kijun_sen)
        
        diff_span_A_with_span_B = difference_from_line(span_a, span_b)
        diff_tenkan_with_kijun = difference_from_line(tenkan_sen, kijun_sen)
        diff_span_A_with_close = difference_from_line(span_a, self.data[CLOSE_COLUMN])
        diff_span_B_with_close = difference_from_line(span_b, self.data[CLOSE_COLUMN])
        diff_kijun_sen_with_close = difference_from_line(kijun_sen, self.data[CLOSE_COLUMN])
        diff_tenkan_sen_with_close = difference_from_line(tenkan_sen, self.data[CLOSE_COLUMN])
    
        self.data['ichimoku_span_A']: span_a
        self.data['ichimoku_span_B']:  span_b
        self.data['ichimoku_kijun_sen']: kijun_sen
        self.data['ichimoku_tenkan_sen']: tenkan_sen
        self.data['ichimoku_tenkan_over_kijun']: tenkan_over_kijun
        self.data['ichimoku_spanaA_over_spanB']: spanaA_over_spanB 
        self.data['ichimoku_price_in_cloud_pos']: price_in_cloud_pos
        self.data['ichimoku_price_in_tenkan_and_kijun_pos']:  price_in_tenkan_and_kijun_pos
        self.data['ichimoku_diff_tenkan_with_kijun']:  diff_tenkan_with_kijun
        self.data['ichimoku_diff_span_A_with_span_B']:  diff_span_A_with_span_B
        self.data['ichimoku_diff_span_A_with_close']:  diff_span_A_with_close
        self.data['ichimoku_diff_span_B_with_close']: diff_span_B_with_close
        self.data['ichimoku_diff_kijun_sen_with_close']: diff_kijun_sen_with_close
        self.data['ichimoku_diff_tenkan_sen_with_close']: diff_tenkan_sen_with_close

    def lch(self):
        print("\tLinear Channel Indicator!")
        self.data['Time'] = np.arange(len(self.data.index))
        lch_in_20_percent_of_band_top = [0]*self.data.shape[0]
        lch_in_20_percent_of_band_bottom = [0]*self.data.shape[0]

        for i in range(100, self.data.shape[0]):
            upper, lower = calc_lch(self.data.loc[i - 100 : i, :])
            lch_in_20_percent_of_band_top[i] = top_of_interval([self.data.loc[i, CLOSE_COLUMN]], upper, lower)[0]
            lch_in_20_percent_of_band_bottom[i] = bottom_of_interval([self.data.loc[i, CLOSE_COLUMN]], upper, lower)[0]

        self.data['lch_in_20_percent_of_band_top'] = lch_in_20_percent_of_band_top
        self.data['lch_in_20_percent_of_band_bottom'] = lch_in_20_percent_of_band_bottom
        self.data = self.data.drop(columns = ['Time'])


    def sr(self):
        print("\tSupport and Resistance!")
        order = 5
        vals = self.data['close'].values
        sr = np.concatenate((get_lows(vals, order), get_highs(vals, order)))
        
        self.data['nearest_sr'] = 0
        self.data['upper_support'] = 0
        self.data['under_resistance'] = 0

        for i in range(len(self.data['close'])):
            self.data.loc[i, 'nearest_sr'] = find_nearest(sr, self.data.loc[i, 'close'])

        self.data.loc[self.data['close'] >= self.data['nearest_sr'], 'upper_support'] = 1
        self.data.loc[self.data['close'] <= self.data['nearest_sr'], 'under_resistance'] = 1

    def divergence(self, indicator):
        print(f'\t{indicator} Divergence!'.format(indicator = indicator))

        if indicator not in self.data.columns:
            print(f'The value of {indicator} does not exist.'.format(indicator = indicator))
            return
        
        self.data = getPeaks(self.data, key = 'close', order = 1, K = 2)
        self.data = getPeaks(self.data, key = indicator, order = 1, K = 2)
        
        indicator_lows = f'{indicator}_lows'.format(indicator = indicator)
        indicator_highs = f'{indicator}_highs'.format(indicator = indicator)
        indicator_hidden_divergence = f'hidden_{indicator}_divergence'.format(indicator = indicator)
        indicator_regular_divergence = f'regular_{indicator}_divergence'.format(indicator = indicator)

        self.data[indicator_hidden_divergence] = 0
        self.data[indicator_regular_divergence] = 0

        for i, (t, row) in enumerate(self.data.iterrows()):
            if np.isnan(row[indicator]):
               continue
            
            if (row['close_highs'] == 1 and row[indicator_highs] == -1) or (row['close_lows'] == 1 and row[indicator_lows] == -1):
                self.data.loc[i, indicator_regular_divergence] = 1
                
            if (row['close_highs'] == -1 and row[indicator_highs] == 1) or (row['close_lows'] == -1 and row[indicator_lows] == 1):
                self.data.loc[i, indicator_hidden_divergence] = 1
        
        self.data = self.data.drop(columns = ['close_highs', 'close_lows', indicator_lows, indicator_highs])
        