from flask import Flask, render_template, request, redirect
import pandas as pd
import os
import sys

sys.path.append("..")

from main import main as run_pipeline

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

    # Dashboard statistics
    total_logs = len(df)
    anomaly_count = len(df[df["anomaly"] == -1])
    normal_count = len(df[df["anomaly"] != -1])

    if total_logs > 0:
        anomaly_percentage = f"{(anomaly_count / total_logs) * 100:.2f}"
    else:
        anomaly_percentage = 0

    return render_template(
        "index.html",
        table=styled_table,
        total_logs=total_logs,
        anomaly_count=anomaly_count,
        normal_count=normal_count,
        anomaly_percentage=anomaly_percentage,
    )


@app.route("/upload", methods=["POST"])
def upload_file():

    file = request.files["logfile"]

    if file.filename == "":
        return redirect("/")

    upload_folder = "../uploads"

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    file_path = os.path.join(upload_folder, file.filename)

    # Save uploaded file
    file.save(file_path)

    # Run AI pipeline on uploaded file
    run_pipeline(file_path=file_path, show_graph=False)

    # Return to dashboard
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)