from utils.libraries import *

def calc_lch(dataframe):
    X = dataframe.loc[:, ['Time']]
    y = dataframe.loc[:, 'close']
    model = LinearRegression()
    model.fit(X, y)

    y_pred = pd.Series(model.predict(X), index = X.index)
    upper = y_pred + np.std(y)
    lower = y_pred - np.std(y)
    
    return [upper.iloc[-1]], [lower.iloc[-1]]