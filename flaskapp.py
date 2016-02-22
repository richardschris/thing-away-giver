from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


class Book:
    claimed = 0
    claimedby = 'NOBODY'
    book_id = 0

    def __init__(self, title, author):
        self.title = title
        self.author = author


@app.route('/')
def book_list():
    connection = sqlite3.connect('book.db')
    cursor = connection.cursor()
    Booklist = create_booklist(cursor)
    return render_template('template.html', booklist=Booklist)


def create_booklist(cursor):
    Booklist = []
    cursor.execute("SELECT * FROM books")
    raw_list = cursor.fetchall()
    for entry in raw_list:
        new_book = Book(entry[0], entry[1])
        new_book.book_id = entry[2]
        new_book.claimed = entry[3]
        new_book.claimedby = entry[4]
        Booklist.append(new_book)
    return Booklist


@app.route('/submit_request', methods=['POST'])
def test_request():
    connection = sqlite3.connect('book.db')
    cursor = connection.cursor()
    claimer_name = ''
    if request.method == 'POST':
        claimer_name = request.form['claimer']
        for entry in request.form:
            if entry == 'Submit':
                continue
            elif entry == 'claimer':
                continue
            else:
                cursor.execute("UPDATE books SET claimedby = ?, claimed = 1 WHERE id = ?", (claimer_name, int(entry)))
                connection.commit()
    connection.close()

    return render_template('submitted.html')


@app.route('/view_results')
def view_results():
    connection = sqlite3.connect('book.db')
    cursor = connection.cursor()
    Booklist = []

    for row in cursor.execute("SELECT * FROM books WHERE claimed = 1"):
        new_book = Book(row[0], row[1])
        new_book.book_id = row[2]
        new_book.claimed = row[3]
        new_book.claimedby = row[4]
        Booklist.append(new_book)

    for row in cursor.execute("SELECT * FROM books WHERE claimed = 2"):
        new_book = Book(row[0], row[1])
        new_book.book_id = row[2]
        new_book.claimed = row[3]
        new_book.claimedby = row[4]
        Booklist.append(new_book)

    connection.close()
    return render_template('results.html', booklist=Booklist)

@app.route('/remove_submission', methods=['POST'])
def remove_submission():
    connection = sqlite3.connect('book.db')
    cursor = connection.cursor()

    print(request.form['submit'])
    if request.method == 'POST' and request.form['submit']=='Remove Submission':
        for entry in request.form:
            if entry == 'submit':
                continue
            else:
                cursor.execute("UPDATE books SET claimedby = ?, claimed = 0 WHERE id = ?", ('NOBODY', int(entry)))
                connection.commit()

    if request.method == 'POST' and request.form['submit']=='Book Given':
        for entry in request.form:
            if entry == 'submit':
                continue
            else:
                cursor.execute("UPDATE books SET claimed = 2 WHERE id = ?", (int(entry),))
                connection.commit()

    connection.close()
    return render_template('submitted.html')

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'GET':
        return render_template('addbook.html')

    if request.method == 'POST':
        connection = sqlite3.connect('book.db')
        cursor = connection.cursor()
        title = request.form['title']
        author = request.form['author']

        cursor.execute("SELECT id FROM books")
        book_id = max(cursor.fetchall())[0] + 1

        book_data = [title, author, book_id]

        cursor.execute("INSERT INTO books VALUES (?, ?, ?, 0, 'NOBODY')", book_data)

        connection.commit()
        connection.close()

        return render_template('submitted.html')


if __name__ == "__main__":
    app.debug = True
    app.run()
