from flask import Flask, render_template
from datetime import datetime
import json

app = Flask(__name__)

def load_notes():
    with open('notes.json', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def home():
    today = datetime.today()
    events = {
        "National Girlfriend Day": datetime(2025, 8, 1),
        "First Unofficial Date Anniversary": datetime(2025, 9, 23),
        "First Official Date Anniversary": datetime(2025, 9, 28),
        "Our 2-Year Anniversary": datetime(2025, 10, 1),
        "Valentine’s Day": datetime(2026, 2, 14)
    }

    countdowns = {}
    for name, date in events.items():
        delta = (date - today).days
        if delta < 0:
            # Count to next year if date passed
            next_year_date = date.replace(year=today.year + 1)
            delta = (next_year_date - today).days
        countdowns[name] = delta

    return render_template('home.html', countdowns=countdowns)

@app.route('/notes')
def notes():
    today = datetime.today().date()
    notes = load_notes()

    for note in notes:
        unlock_date = datetime.strptime(note["date"], "%Y-%m-%d").date()
        note["unlocked"] = today >= unlock_date

    return render_template('notes.html', notes=notes)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))  # Use Render’s PORT env variable or default to 5000
    app.run(host='0.0.0.0', port=port, debug=True)
