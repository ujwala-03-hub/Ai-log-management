import matplotlib.pyplot as plt
import os

def plot_data(df):

    plt.figure(figsize=(6,4))

    df['anomaly'].value_counts().plot(kind='bar')

    plt.title("Anomaly Detection")
    plt.xlabel("Normal (1) vs Anomaly (-1)")
    plt.ylabel("Count")

    # Save graph inside app/static folder
    save_path = os.path.join(
        os.path.dirname(__file__),
        "../../app/static/anomaly_chart.png"
    )

    plt.savefig(save_path, bbox_inches="tight")
    plt.close()