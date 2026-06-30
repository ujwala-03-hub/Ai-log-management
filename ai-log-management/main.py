from src.preprocessing.parse_logs import load_logs
from src.features.build_features import create_features
from src.models.anomaly_detection import detect_anomalies
from src.visualization.visualize import plot_data

def main():
    df = load_logs()
    
    df = create_features(df)
    
    df = detect_anomalies(df)
    
    # ✅ Save full data
    df.to_csv("outputs/anomalies.csv", index=False)
    
    # ✅ Save only anomalies
    anomalies = df[df['anomaly'] == -1]
    anomalies.to_csv("outputs/predictions.csv", index=False)

    # ✅ ADD SUMMARY CODE HERE 👇
    total = len(df)
    anomaly_count = len(df[df['anomaly'] == -1])

    with open("outputs/reports/summary.txt", "w") as f:
        f.write(f"Total Logs: {total}\n")
        f.write(f"Anomalies: {anomaly_count}\n")

    print(df)
    
    plot_data(df)

if __name__ == "__main__":
    main()