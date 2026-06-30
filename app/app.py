from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    # Read the anomalies CSV
    df = pd.read_csv("../outputs/anomalies.csv")

    # Highlight anomaly rows in red
    def highlight(row):
        return [
            "background-color: red" if row["anomaly"] == -1 else ""
            for _ in row
        ]

    # Convert the styled DataFrame to HTML
    styled_table = df.style.apply(highlight, axis=1).to_html()

    # Calculate dashboard statistics
    total_logs = len(df)
    anomaly_count = len(df[df["anomaly"] == -1])
    normal_count = len(df[df["anomaly"] != -1])

    # Calculate anomaly percentage safely
    if total_logs > 0:
        anomaly_percentage = f"{(anomaly_count / total_logs) * 100:.2f}"
    else:
        anomaly_percentage = 0

    # Render the dashboard
    return render_template(
        "index.html",
        table=styled_table,
        total_logs=total_logs,
        anomaly_count=anomaly_count,
        normal_count=normal_count,
        anomaly_percentage=anomaly_percentage,
    )

if __name__ == "__main__":
    app.run(debug=True)