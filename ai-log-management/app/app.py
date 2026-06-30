from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    df = pd.read_csv("../outputs/anomalies.csv")

    # Highlight anomalies in red 🚨
    def highlight(row):
        return ['background-color: red' if row['anomaly'] == -1 else '' for _ in row]

    styled_table = df.style.apply(highlight, axis=1).to_html()

    return render_template("index.html", table=styled_table)

if __name__ == "__main__":
    app.run(debug=True)