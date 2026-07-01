from flask import Flask, render_template, request, redirect, send_file
import pandas as pd
import os
import sys

sys.path.append("..")

from main import main as run_pipeline

app = Flask(__name__)


@app.route("/")
def home():

    # Get success message from URL
    success = request.args.get("success")

    # Read latest output
    df = pd.read_csv("../outputs/anomalies.csv")

    # Highlight anomalies
    def highlight(row):
        return [
            "background-color:red;color:white;" if row["anomaly"] == -1 else ""
            for _ in row
        ]

    styled_table = df.style.apply(highlight, axis=1).to_html()

    # Dashboard statistics
    total_logs = len(df)
    anomaly_count = len(df[df["anomaly"] == -1])
    normal_count = len(df[df["anomaly"] != -1])

    if total_logs > 0:
        anomaly_percentage = f"{(anomaly_count/total_logs)*100:.2f}"
    else:
        anomaly_percentage = "0.00"

    return render_template(
        "index.html",
        table=styled_table,
        total_logs=total_logs,
        anomaly_count=anomaly_count,
        normal_count=normal_count,
        anomaly_percentage=anomaly_percentage,
        success=success
    )


@app.route("/upload", methods=["POST"])
def upload_file():

    if "logfile" not in request.files:
        return redirect("/")

    file = request.files["logfile"]

    if file.filename == "":
        return redirect("/")

    upload_folder = "../uploads"

    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, file.filename)

    # Save uploaded file
    file.save(file_path)

    # Run AI Pipeline
    run_pipeline(file_path=file_path, show_graph=False)

    # Redirect with success message
    return redirect("/?success=1")


# ---------------- DOWNLOAD ANOMALIES ----------------
@app.route("/download/anomalies")
def download_anomalies():
    return send_file(
        "../outputs/anomalies.csv",
        as_attachment=True
    )


# ---------------- DOWNLOAD SUMMARY ----------------
@app.route("/download/summary")
def download_summary():
    return send_file(
        "../outputs/reports/summary.txt",
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)