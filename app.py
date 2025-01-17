from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def db():
    with sqlite3.connect("database.db") as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending'
        )
        """)
        print("Database created successfully")

@app.route('/')
def index():
    with sqlite3.connect("database.db") as conn:
        tasks = conn.execute("SELECT * FROM tasks").fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    if task:
        with sqlite3.connect("database.db") as conn:
            conn.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
        return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    with sqlite3.connect("database.db") as conn:
        conn.execute("DELETE FROM tasks WHERE id=?", (id,))
    return redirect('/')

@app.route('/update/<int:id>')
def update(id):
    with sqlite3.connect("database.db") as conn:
        task = conn.execute("SELECT * FROM tasks WHERE id=?", (id,)).fetchone()
    return render_template('update.html', task=task)

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    with sqlite3.connect("database.db") as conn:
        current_status = conn.execute("SELECT status FROM tasks WHERE id = ?", (task_id,)).fetchone()
        new_status = 'pending' if current_status[0] == 'completed' else 'completed'
        conn.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
    return ('', 204)

if __name__ == '__main__':
    db()
    app.run(debug=True)