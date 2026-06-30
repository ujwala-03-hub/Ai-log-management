import pandas as pd

def load_logs():
    df = pd.read_csv("data/sample/demo_logs.csv")
    return df