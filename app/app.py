from flask import Flask, render_template, request, redirect, send_file
import pandas as pd
import os
import sys

sys.path.append("..")

from main import main as run_pipeline

app = Flask(__name__)


@app.route("/")
def home():

    # Success message
    success = request.args.get("success")

    # Read latest output
    df = pd.read_csv("../outputs/anomalies.csv")

    # ---------------- Highlight anomaly rows ----------------
    def highlight(row):
        return [
            "background-color:red;color:white;" if row["anomaly"] == -1 else ""
            for _ in row
        ]

    # ---------------- Color Status Column ----------------
    def color_status(val):
        if val >= 500:
            return "background-color:#ff4d4d;color:white;font-weight:bold;"
        elif val >= 400:
            return "background-color:#ffc107;color:black;font-weight:bold;"
        elif val >= 200:
            return "background-color:#28a745;color:white;font-weight:bold;"
        return ""

    # ---------------- Full Table ----------------
    styled_table = (
        df.style
        .apply(highlight, axis=1)
        .map(color_status, subset=["status"])
        .to_html()
    )

    # ---------------- Recent Anomalies ----------------
    recent_anomalies = df[df["anomaly"] == -1].head(10)

    recent_table = (
        recent_anomalies.style
        .apply(highlight, axis=1)
        .map(color_status, subset=["status"])
        .hide(axis="index")
        .to_html()
    )

    # ---------------- Top 5 IP Addresses ----------------
    top_ips = (
        df["ip"]
        .value_counts()
        .head(5)
        .reset_index()
    )

    top_ips.columns = ["IP Address", "Requests"]

    top_ips_table = (
        top_ips.style
        .hide(axis="index")
        .to_html()
    )

    # ---------------- Dashboard Statistics ----------------
    total_logs = len(df)
    anomaly_count = len(df[df["anomaly"] == -1])
    normal_count = len(df[df["anomaly"] != -1])

    if total_logs > 0:
        anomaly_percentage = f"{(anomaly_count / total_logs) * 100:.2f}"
    else:
        anomaly_percentage = "0.00"

    return render_template(
        "index.html",
        table=styled_table,
        recent_table=recent_table,
        top_ips_table=top_ips_table,
        total_logs=total_logs,
        anomaly_count=anomaly_count,
        normal_count=normal_count,
        anomaly_percentage=anomaly_percentage,
        success=success
    )


# ---------------- Upload CSV ----------------
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

    file.save(file_path)

    run_pipeline(file_path=file_path, show_graph=False)

    return redirect("/?success=1")


# ---------------- Download Anomalies ----------------
@app.route("/download/anomalies")
def download_anomalies():
    return send_file(
        "../outputs/anomalies.csv",
        as_attachment=True
    )


# ---------------- Download Summary ----------------
@app.route("/download/summary")
def download_summary():
    return send_file(
        "../outputs/reports/summary.txt",
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)