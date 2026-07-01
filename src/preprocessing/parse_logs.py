import pandas as pd

def load_logs(file_path="data/sample/demo_logs.csv"):
    df = pd.read_csv(file_path)
    return df 