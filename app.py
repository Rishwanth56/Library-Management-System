from flask import Flask, render_template, request, redirect, flash
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "library123"

def get_connection():
    conn = sqlite3.connect("library.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- HOME ----------------

@app.route("/")
def index():

    conn = get_connection()

    books = conn.execute(
        "SELECT * FROM books"
    ).fetchall()

    total_books = conn.execute(
        "SELECT COUNT(*) FROM books"
    ).fetchone()[0]

    available_books = conn.execute(
        "SELECT IFNULL(SUM(quantity),0) FROM books"
    ).fetchone()[0]

    issued_books = conn.execute("""
        SELECT COUNT(*)
        FROM issued_books
        JOIN books
        ON books.id = issued_books.book_id
    """).fetchone()[0]

    conn.close()

    return render_template(
        "index.html",
        books=books,
        total_books=total_books,
        available_books=available_books,
        issued_books=issued_books
    )


# ---------------- ADD BOOK ----------------

@app.route("/add", methods=["GET", "POST"])
def add_book():

    if request.method == "POST":

        title = request.form["title"]
        author = request.form["author"]
        category = request.form["category"]
        quantity = request.form["quantity"]

        conn = get_connection()

        conn.execute(
            """
            INSERT INTO books
            (title,author,category,quantity)
            VALUES(?,?,?,?)
            """,
            (title, author, category, quantity)
        )

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add_book.html")


# ---------------- EDIT BOOK ----------------

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_book(id):

    conn = get_connection()

    if request.method == "POST":

        title = request.form["title"]
        author = request.form["author"]
        category = request.form["category"]
        quantity = request.form["quantity"]

        conn.execute(
            """
            UPDATE books
            SET title=?,author=?,category=?,quantity=?
            WHERE id=?
            """,
            (title, author, category, quantity, id)
        )

        conn.commit()
        conn.close()

        return redirect("/")

    book = conn.execute(
        "SELECT * FROM books WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template(
        "edit_book.html",
        book=book
    )


# ---------------- DELETE BOOK ----------------

@app.route("/delete/<int:id>")
def delete_book(id):

    conn = get_connection()

    issued = conn.execute(
        "SELECT COUNT(*) FROM issued_books WHERE book_id=?",
        (id,)
    ).fetchone()[0]

    if issued > 0:
        conn.close()
        flash("❌ Cannot delete! This book is currently issued.", "danger")
        return redirect("/")

    conn.execute(
        "DELETE FROM books WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    flash("✅ Book deleted successfully.", "success")

    return redirect("/")

# ---------------- SEARCH ----------------

@app.route("/search")
def search():

    keyword = request.args.get("keyword", "")

    conn = get_connection()

    books = conn.execute(
        """
        SELECT * FROM books
        WHERE title LIKE ?
        OR author LIKE ?
        """,
        ('%' + keyword + '%', '%' + keyword + '%')
    ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        books=books,
        total_books=len(books),
        available_books=sum(book["quantity"] for book in books),
        issued_books=0
    )
# ---------------- ISSUE BOOK ----------------

@app.route("/issue/<int:id>", methods=["GET","POST"])
def issue_book(id):

    conn = get_connection()

    book = conn.execute(
        "SELECT * FROM books WHERE id=?",
        (id,)
    ).fetchone()

    if book["quantity"] <= 0:
        conn.close()
        flash("❌ This book is out of stock and cannot be issued.", "warning")
        return redirect("/")

    if request.method == "POST":

        student = request.form["student"]
        roll = request.form["roll"]

        issue_date = datetime.now()
        return_date = issue_date + timedelta(days=14)

        conn.execute(
            """
            INSERT INTO issued_books
            (student_name,roll_no,book_id,issue_date,return_date)
            VALUES(?,?,?,?,?)
            """,
            (
                student,
                roll,
                id,
                issue_date.strftime("%d-%m-%Y"),
                return_date.strftime("%d-%m-%Y")
            )
        )

        conn.execute(
            "UPDATE books SET quantity=quantity-1 WHERE id=?",
            (id,)
        )

        conn.commit()
        conn.close()

        flash("✅ Book issued successfully.", "success")

        return redirect("/")

    conn.close()

    return render_template(
        "issue_book.html",
        book=book
    )

# ---------------- RETURN BOOK ----------------

@app.route("/return/<int:id>")
def return_book(id):

    conn = get_connection()

    issue = conn.execute(
        "SELECT * FROM issued_books WHERE book_id=? LIMIT 1",
        (id,)
    ).fetchone()

    if issue:

        conn.execute(
            "DELETE FROM issued_books WHERE id=?",
            (issue["id"],)
        )

        conn.execute(
            "UPDATE books SET quantity = quantity + 1 WHERE id=?",
            (id,)
        )

        conn.commit()

    conn.close()

    return redirect("/")


# ---------------- ISSUED BOOKS ----------------

@app.route("/issued")
def issued():

    conn = get_connection()

    books = conn.execute(
        """
        SELECT
            issued_books.id,
            student_name,
            roll_no,
            books.title,
            issue_date,
            return_date
        FROM issued_books
        JOIN books
        ON books.id = issued_books.book_id
        """
    ).fetchall()

    conn.close()

    return render_template(
        "issued_books.html",
        books=books
    )


# ---------------- RUN APP ----------------

if __name__ == "__main__":
    app.run(debug=True)
