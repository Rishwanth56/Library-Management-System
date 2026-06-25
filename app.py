from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_connection():
    conn = sqlite3.connect("library.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_connection()
    books = conn.execute("SELECT * FROM books").fetchall()
    conn.close()
    return render_template("index.html", books=books)

@app.route("/add", methods=["GET","POST"])
def add_book():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        category = request.form["category"]
        quantity = int(request.form["quantity"])

        conn = get_connection()
        conn.execute(
            "INSERT INTO books(title,author,category,quantity) VALUES(?,?,?,?)",
            (title, author, category, quantity)
        )
        conn.commit()
        conn.close()
        return redirect("/")

    return render_template("add_book.html")

@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit_book(id):
    conn = get_connection()

    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        category = request.form["category"]
        quantity = int(request.form["quantity"])

        conn.execute(
            "UPDATE books SET title=?,author=?,category=?,quantity=? WHERE id=?",
            (title, author, category, quantity, id)
        )
        conn.commit()
        conn.close()
        return redirect("/")

    book = conn.execute("SELECT * FROM books WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("edit_book.html", book=book)

@app.route("/delete/<int:id>")
def delete_book(id):
    conn = get_connection()
    conn.execute("DELETE FROM books WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/search")
def search():
    keyword = request.args.get("keyword","")
    conn = get_connection()
    books = conn.execute(
        "SELECT * FROM books WHERE title LIKE ? OR author LIKE ?",
        (f"%{keyword}%", f"%{keyword}%")
    ).fetchall()
    conn.close()
    return render_template("index.html", books=books)

@app.route("/issue/<int:id>", methods=["GET","POST"])
def issue_book(id):
    conn = get_connection()

    if request.method == "POST":
        student = request.form["student"]
        book = conn.execute(
            "SELECT * FROM books WHERE id=?", (id,)
        ).fetchone()

        if book["quantity"] > 0:
            conn.execute(
                "INSERT INTO issued_books(student_name,book_id,issue_date) VALUES(?,?,?)",
                (student, id, datetime.now().strftime("%d-%m-%Y"))
            )
            conn.execute(
                "UPDATE books SET quantity=quantity-1 WHERE id=?", (id,)
            )
            conn.commit()

        conn.close()
        return redirect("/")

    book = conn.execute("SELECT * FROM books WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("issue_book.html", book=book)

@app.route("/return/<int:id>")
def return_book(id):
    conn = get_connection()

    issue = conn.execute(
        "SELECT * FROM issued_books WHERE book_id=? LIMIT 1", (id,)
    ).fetchone()

    if issue:
        conn.execute("DELETE FROM issued_books WHERE id=?", (issue["id"],))
        conn.execute(
            "UPDATE books SET quantity=quantity+1 WHERE id=?", (id,)
        )
        conn.commit()

    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
