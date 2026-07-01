import os
from src.preprocessing.parse_logs import load_logs
from src.features.build_features import create_features
from src.models.anomaly_detection import detect_anomalies
from src.visualization.visualize import plot_data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main(file_path="data/sample/demo_logs.csv", show_graph=True):

    df = load_logs(file_path)
    print("Uploaded file loaded successfully!")
    print(df.head())

    df = create_features(df)

    df = detect_anomalies(df)

    # Save full data
    anomalies_path = os.path.join(BASE_DIR, "outputs", "anomalies.csv")
    df.to_csv(anomalies_path, index=False)

    # Save only anomalies
    anomalies = df[df['anomaly'] == -1]
    predictions_path = os.path.join(BASE_DIR, "outputs", "predictions.csv")
    anomalies.to_csv(predictions_path, index=False)
    total = len(df)
    anomaly_count = len(df[df['anomaly'] == -1])

    summary_path = os.path.join(BASE_DIR, "outputs", "reports", "summary.txt")
    with open(summary_path, "w") as f:
     f.write(f"Total Logs: {total}\n")
     f.write(f"Anomalies: {anomaly_count}\n")

    print(df)

    if show_graph:
        plot_data(df)

if __name__ == "__main__":
    main()