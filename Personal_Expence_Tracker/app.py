from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("expenses.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create table if not exists
conn = get_db_connection()
conn.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    amount REAL NOT NULL
)
""")
conn.commit()
conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db_connection()

    if request.method == "POST":
        title = request.form["title"]
        amount = request.form["amount"]
        conn.execute(
            "INSERT INTO expenses (title, amount) VALUES (?, ?)",
            (title, amount)
        )
        conn.commit()

    expenses = conn.execute("SELECT * FROM expenses").fetchall()
    conn.close()
    return render_template("index.html", expenses=expenses)

@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM expenses WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
