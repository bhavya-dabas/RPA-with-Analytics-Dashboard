from flask import Flask, render_template
import sys
sys.path.insert(0, '../backend')
from db_utils import get_stats, fetch_logs

app = Flask(__name__)

@app.route('/')
def dashboard():
    stats = get_stats()
    logs = fetch_logs()
    return render_template('dashboard.html', stats=stats, logs=logs)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
