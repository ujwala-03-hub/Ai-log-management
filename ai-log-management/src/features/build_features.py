def create_features(df):
    df['is_error'] = df['status'].apply(lambda x: 1 if x >= 400 else 0)
    df['request_count'] = df.groupby('ip')['ip'].transform('count')

    # NEW FEATURES 🔥
    df['error_ratio'] = df['is_error'] / df['request_count']
    df['status_group'] = df['status'] // 100

    return df