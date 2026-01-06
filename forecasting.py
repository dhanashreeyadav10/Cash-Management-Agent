
import numpy as np
from sklearn.linear_model import LinearRegression

def forecast_series(series, days=30):
    y = series.values
    X = np.arange(len(y)).reshape(-1, 1)

    model = LinearRegression()
    model.fit(X, y)

    future_X = np.arange(len(y), len(y) + days).reshape(-1, 1)
    return model.predict(future_X)

