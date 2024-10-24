from flask import Flask, render_template, request, redirect, url_for
from models import db, Event

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
db.init_app(app)

@app.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', events=events)

@app.route('/add', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        time = request.form['time']
        description = request.form.get('description', '')
        reminder = request.form.get('reminder', 0)

        new_event = Event(title=title, date=date, time=time, description=description, reminder=reminder)
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_event.html')
