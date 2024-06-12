import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS crops (id INTEGER PRIMARY KEY, name TEXT, quantity INTEGER, operation TEXT, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY, name TEXT, amount REAL, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS incomes (id INTEGER PRIMARY KEY, source TEXT, amount REAL, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_crop', methods=['GET', 'POST'])
def add_crop():
    if request.method == 'POST':
        crop_name = request.form['crop_name']
        quantity = int(request.form['quantity'])
        operation = request.form['operation']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        if operation == 'شراء':
            cursor.execute('INSERT INTO crops (name, quantity, operation) VALUES (?, ?, ?)', (crop_name, quantity, operation))
        elif operation == 'بيع':
            cursor.execute('UPDATE crops SET quantity = quantity - ? WHERE name = ?', (quantity, crop_name))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_crop.html')

@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        expense_name = request.form['expense_name']
        amount = request.form['amount']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO expenses (name, amount) VALUES (?, ?)', (expense_name, amount))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_expense.html')

@app.route('/add_income', methods=['GET', 'POST'])
def add_income():
    if request.method == 'POST':
        income_source = request.form['income_source']
        amount = request.form['amount']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO incomes (source, amount) VALUES (?, ?)', (income_source, amount))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_income.html')

@app.route('/view_data')
def view_data():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM crops')
    crops = cursor.fetchall()
    
    cursor.execute('SELECT * FROM expenses')
    expenses = cursor.fetchall()
    
    cursor.execute('SELECT * FROM incomes')
    incomes = cursor.fetchall()
    
    cursor.execute('SELECT SUM(quantity) FROM crops')
    total_crops = cursor.fetchone()[0]
    
    cursor.execute('SELECT SUM(amount) FROM expenses')
    total_expenses = cursor.fetchone()[0]
    
    cursor.execute('SELECT SUM(amount) FROM incomes')
    total_incomes = cursor.fetchone()[0]
    
    conn.close()
    
    return render_template('view_data.html', crops=crops, expenses=expenses, incomes=incomes, total_crops=total_crops, total_expenses=total_expenses, total_incomes=total_incomes)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
