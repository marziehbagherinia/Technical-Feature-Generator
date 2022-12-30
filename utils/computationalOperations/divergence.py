from utils.libraries import *
def getHigherLows(data: np.array, order = 1, K = 2):
  # Get highs
  low_idx = argrelextrema(data, np.less, order = order)[0]
  lows = data[low_idx]

  # Ensure consecutive highs are higher than previous highs
  extrema = []
  ex_deque = deque(maxlen = K)
  for i, idx in enumerate(low_idx):
    if i == 0:
      ex_deque.append(idx)
      continue
    if lows[i] < lows[i-1]:
      ex_deque.clear()

    ex_deque.append(idx)
    if len(ex_deque) == K:
      extrema.append(ex_deque.copy())

  return extrema

def getLowerHighs(data: np.array, order = 1, K = 2):
  # Get highs
  high_idx = argrelextrema(data, np.greater, order = order)[0]
  highs = data[high_idx]

  # Ensure consecutive highs are lower than previous highs
  extrema = []
  ex_deque = deque(maxlen = K)
  for i, idx in enumerate(high_idx):
    if i == 0:
      ex_deque.append(idx)
      continue
    if highs[i] > highs[i-1]:
      ex_deque.clear()

    ex_deque.append(idx)
    if len(ex_deque) == K:
      extrema.append(ex_deque.copy())

  return extrema

def getHigherHighs(data: np.array, order = 1, K = 2):
  # Get highs
  high_idx = argrelextrema(data, np.greater, order = order)[0]
  highs = data[high_idx]

  # Ensure consecutive highs are higher than previous highs
  extrema = []
  ex_deque = deque(maxlen = K)
  for i, idx in enumerate(high_idx):
    if i == 0:
      ex_deque.append(idx)
      continue
    if highs[i] < highs[i-1]:
      ex_deque.clear()

    ex_deque.append(idx)
    if len(ex_deque) == K:
      extrema.append(ex_deque.copy())

  return extrema

def getLowerLows(data: np.array, order = 1, K = 2):
  # Get lows
  low_idx = argrelextrema(data, np.less, order = order)[0]
  lows = data[low_idx]

  # Ensure consecutive lows are lower than previous lows
  extrema = []
  ex_deque = deque(maxlen = K)
  for i, idx in enumerate(low_idx):
    if i == 0:
      ex_deque.append(idx)
      continue
    if lows[i] > lows[i-1]:
      ex_deque.clear()

    ex_deque.append(idx)
    if len(ex_deque) == K:
      extrema.append(ex_deque.copy())

  return extrema

def getHHIndex(data: np.array, order = 1, K = 2):
  extrema = getHigherHighs(data, order, K)
  idx = np.array([i[-1] for i in extrema])
  return idx[np.where(idx < len(data))]

def getLHIndex(data: np.array, order = 1, K = 2):
  extrema = getLowerHighs(data, order, K)
  idx = np.array([i[-1] for i in extrema])
  return idx[np.where(idx < len(data))]

def getLLIndex(data: np.array, order = 1, K = 2):
  extrema = getLowerLows(data, order, K)
  idx = np.array([i[-1] for i in extrema])
  return idx[np.where(idx < len(data))]

def getHLIndex(data: np.array, order = 1, K = 2):
  extrema = getHigherLows(data, order, K)
  idx = np.array([i[-1] for i in extrema])
  return idx[np.where(idx < len(data))]

def getPeaks(data, key = 'close', order = 1, K = 2):
  vals = data[key].values
  hh_idx = getHHIndex(vals, order, K)
  lh_idx = getLHIndex(vals, order, K)
  ll_idx = getLLIndex(vals, order, K)
  hl_idx = getHLIndex(vals, order, K)
  
  data[f'{key}_highs'] = 0
  data[f'{key}_highs'][hh_idx] = 1
  data[f'{key}_highs'][lh_idx] = -1
  data[f'{key}_lows'] = 0
  data[f'{key}_lows'][ll_idx] = 1
  data[f'{key}_lows'][hl_idx] = -1
  return data