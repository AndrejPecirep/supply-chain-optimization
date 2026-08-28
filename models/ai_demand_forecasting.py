from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.model_selection import train_test_split
from utils.io import RAW, OUTPUT


def _features(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data['order_date'] = pd.to_datetime(data['order_date'])
    data['dayofweek'] = data['order_date'].dt.dayofweek
    data['month'] = data['order_date'].dt.month
    data['dayofyear'] = data['order_date'].dt.dayofyear
    data['is_weekend'] = data['dayofweek'].isin([5, 6]).astype(int)
    data = pd.get_dummies(data, columns=['sku','customer_segment','region'], drop_first=False)
    return data


def train_forecast_model(input_path: Path = RAW/'customer_orders_demand.csv') -> tuple[RandomForestRegressor, float, list[str]]:
    df = pd.read_csv(input_path)
    data = _features(df)
    y = data['quantity']
    X = data.drop(columns=['quantity','order_date'])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, shuffle=False)
    model = RandomForestRegressor(n_estimators=120, random_state=42, min_samples_leaf=2)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    mape = mean_absolute_percentage_error(y_test, predictions)
    return model, float(mape), list(X.columns)


def create_future_forecast(days: int = 90) -> pd.DataFrame:
    source = pd.read_csv(RAW/'customer_orders_demand.csv')
    model, mape, feature_columns = train_forecast_model()
    last_date = pd.to_datetime(source['order_date']).max()
    skus = sorted(source['sku'].unique())
    rows = []
    for day in range(1, days + 1):
        for sku in skus:
            base = {
                'order_date': last_date + pd.Timedelta(days=day),
                'sku': sku,
                'customer_segment': 'B2B',
                'price': float(source[source['sku'] == sku]['price'].median()),
                'promotion_flag': 0,
                'region': 'BA',
            }
            rows.append(base)
    future = pd.DataFrame(rows)
    features = _features(future).drop(columns=['order_date'])
    for col in feature_columns:
        if col not in features.columns:
            features[col] = 0
    features = features[feature_columns]
    future['forecast_quantity'] = np.maximum(0, model.predict(features)).round().astype(int)
    future['model_mape'] = round(mape, 4)
    return future[['order_date','sku','forecast_quantity','model_mape']]

if __name__ == '__main__':
    OUTPUT.mkdir(parents=True, exist_ok=True)
    forecast = create_future_forecast()
    forecast.to_csv(OUTPUT/'demand_forecast_90_days.csv', index=False)
    print(forecast.head())
