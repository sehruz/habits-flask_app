import uuid
from flask import Blueprint, current_app, redirect, render_template, request, url_for
import datetime
from collections import defaultdict


pages=Blueprint('habits',__name__, template_folder='templates', static_folder='static')



def datetime_func():
    date=datetime.datetime.today()
    return datetime.datetime(date.year, date.month, date.day)

@pages.context_processor
def range_finder():
    def date_range(start: datetime.datetime):
        dates=[start + datetime.timedelta(days=diff) for diff in range(-3,4)]
        return dates
    return {'date_range':date_range}


@pages.route('/')
def index():
    date_str=request.args.get('date')
    if date_str:
        selected_date=datetime.datetime.fromisoformat(date_str)
    else:
        selected_date=datetime_func()
    habits_current_day= current_app.db.habits.find({'date': {'$lte': selected_date}})
    
    completions=[ habit['habit'] for habit in current_app.db.completions.find({'date': selected_date})]
    
    return render_template('index.html',
     habits=habits_current_day,
     title='Habit Tracker - Home',
     selected_date=selected_date,
     completions=completions
     )



@pages.route('/add/', methods=['GET','POST'])
def add_habit():
    if request.method=='POST':
       current_app.db.habits.insert_one({'_id': uuid.uuid4().hex, 'name': request.form.get('habit'), 'date': datetime_func() })
   
    return render_template('add_habit.html', title='Habit Tracker - Add Habit', selected_date=datetime.datetime.today() )


@pages.route('/complete', methods=['POST'])
def complete():
    date_str=request.form.get('date')
    habit=request.form.get('habitId')
    date=datetime.datetime.fromisoformat(date_str)
    current_app.db.completions.insert_one({'date': date, 'habit':habit })

    return redirect(url_for('habits.index', date=date_str))


