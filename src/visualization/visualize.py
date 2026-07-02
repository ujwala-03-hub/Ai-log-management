import matplotlib.pyplot as plt
import os
import traceback

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

STATIC_FOLDER = os.path.join(BASE_DIR, "app", "static")
os.makedirs(STATIC_FOLDER, exist_ok=True)


def plot_data(df):

    charts = [
        ("anomaly_chart.png", lambda: (
            plt.figure(figsize=(6,4)),
            df["anomaly"].value_counts().plot(kind="bar"),
            plt.title("Normal vs Anomalies"),
            plt.tight_layout(),
            plt.savefig(os.path.join(STATIC_FOLDER, "anomaly_chart.png")),
            plt.close()
        )),

        ("pie_chart.png", lambda: (
            plt.figure(figsize=(5,5)),
            df["anomaly"].value_counts().plot(kind="pie", autopct="%1.1f%%"),
            plt.ylabel(""),
            plt.title("Anomaly Distribution"),
            plt.tight_layout(),
            plt.savefig(os.path.join(STATIC_FOLDER, "pie_chart.png")),
            plt.close()
        )),

        ("status_chart.png", lambda: (
            plt.figure(figsize=(7,4)),
            df["status"].value_counts().sort_index().plot(kind="bar"),
            plt.title("HTTP Status Codes"),
            plt.tight_layout(),
            plt.savefig(os.path.join(STATIC_FOLDER, "status_chart.png")),
            plt.close()
        )),

        ("method_chart.png", lambda: (
            plt.figure(figsize=(7,4)),
            df["method"].value_counts().plot(kind="bar"),
            plt.title("HTTP Request Methods"),
            plt.tight_layout(),
            plt.savefig(os.path.join(STATIC_FOLDER, "method_chart.png")),
            plt.close()
        ))
    ]

    for filename, chart in charts:
        try:
            print(f"Creating {filename}...")
            chart()
            print(f"✅ {filename} created")
        except Exception:
            print(f"❌ Error while creating {filename}")
            traceback.print_exc()

    print("Finished plotting.")