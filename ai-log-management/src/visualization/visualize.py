import matplotlib.pyplot as plt

def plot_data(df):
    df['anomaly'].value_counts().plot(kind='bar')
    plt.title("Anomaly Detection")
    plt.xlabel("Normal (1) vs Anomaly (-1)")
    plt.ylabel("Count")
    plt.show()