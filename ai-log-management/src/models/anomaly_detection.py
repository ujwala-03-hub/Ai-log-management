from sklearn.ensemble import IsolationForest

def detect_anomalies(df):
    model = IsolationForest(contamination=0.3, random_state=42)

    df['anomaly'] = model.fit_predict(
        df[['status', 'request_count', 'error_ratio']]
    )

    return df