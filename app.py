from flask import Flask, render_template, g, request
import sqlite3
from datetime import datetime
from database import connect_db, get_db

app = Flask(__name__)




@app.teardown_appcontext
def close_connection(exception):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/home', methods=['GET', 'POST'])
def view():
    db = get_db()
    if request.method == 'POST':
        date = request.form['date-form']
        # editing user-input date to add in db
        date_to_format = datetime.strptime(date, '%Y-%m-%d')
        db_date_format = datetime.strftime(date_to_format, '%Y%m%d')
        db.execute('INSERT INTO date_id (entry_date) VALUES (?)', [db_date_format])
        db.commit()

    cur = db.execute(
        '''
     SELECT
     date_id.entry_date As entry_date,
     SUM(food.protein) AS protein, 
     SUM(food.carbohydrates) AS carbohydrates,
     SUM(food.fats) AS fats,
     SUM(food.calories) AS calories
     FROM date_id
     LEFT JOIN  dateid_foodid ON date_id.date_id = dateid_foodid.date_id
     LEFT JOIN  food ON food.food_id = dateid_foodid.food_id
     GROUP BY date_id.date_id
     ORDER BY entry_date DESC
     ''')
    query_results = cur.fetchall()
    display_results = []

    for el in query_results:
        single_res = dict()
        single_res['protein'] = el['protein']
        single_res['carbohydrates'] = el['carbohydrates']
        single_res['fats'] = el['fats']
        single_res['calories'] = el['calories']
        # preparing 2 formats of data: for displaying and for storing in db
        date_input = datetime.strptime(str(el['entry_date']), '%Y%m%d')
        to_db_date = datetime.strftime(date_input, '%Y%m%d')
        single_res['db_date'] = to_db_date
        single_res['pretty_date'] = datetime.strftime(date_input, '%B, %D, %Y')
        display_results.append(single_res)
    return render_template('home.html', display_results=display_results,  classname='active')


@app.route('/detail/<date>', methods=['GET', 'POST'])
def detail(date):
    db = get_db()

    curr_date = db.execute('SELECT date_id FROM date_id WHERE entry_date = (?)', [date])
    date_id = curr_date.fetchone()['date_id']

    if request.method == 'POST':

        food_instance = request.form['food-select']
        db.execute('''
        INSERT INTO dateid_foodid
        (date_id, food_id)
        VALUES (?, ?)''',
                   [date_id, food_instance])
        db.commit()

    # Selecting food info to display
    food_cur = db.execute(
        '''
     SELECT 
     food.food_name AS food_name, 
     food.protein AS protein, 
     food.carbohydrates AS carbohydrates,
     food.fats AS fats,
     food.calories AS calories
     FROM food
     JOIN dateid_foodid ON food.food_id = dateid_foodid.food_id
     JOIN date_id ON dateid_foodid.date_id = date_id.date_id
     WHERE date_id.date_id = (?) 
     ''', [date_id])
    food_results = food_cur.fetchall()

    total_display_res = {
        'protein': 0,
        'carbohydrates':0,
        'fats':0,
        'calories':0
    }


    for el in food_results:
        total_display_res['protein'] += el['protein']
        total_display_res['carbohydrates'] += el['carbohydrates']
        total_display_res['fats'] += el['fats']
        total_display_res['calories'] += el['calories']



    # Selecting choice field options
    options_cur = db.execute('SELECT * FROM food')
    food_options = options_cur.fetchall()

    # prettifying date to display
    input_date = datetime.strptime(date, '%Y%m%d')
    display_format_date = datetime.strftime(input_date, '%B %d, %Y')

    return render_template('detail.html',
                           date=display_format_date, food_results=food_results,
                           food_options=food_options, total=total_display_res)


@app.route('/addfood', methods=['GET', 'POST'])
def add_item():
    db = get_db()

    if request.method == 'POST':
        food_name = request.form['food_name']
        protein = int(request.form['protein'])
        carbohydrates = int(request.form['carbohydrates'])
        fats = int(request.form['fats'])
        calories = protein * 4 + carbohydrates * 4 + fats * 9

        db.execute('''INSERT INTO food
         (food_name, protein, carbohydrates, fats, calories)
         VALUES (?, ?, ?, ?, ?)''',
                   [food_name, protein, carbohydrates, fats, calories])
        db.commit()
    results = db.execute('SELECT * FROM food')

    return render_template('add_item.html', results=results, classname1='active')


if __name__ == '__main__':
    app.run(debug=True)
