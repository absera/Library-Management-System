from flask import render_template, Flask, redirect, url_for, request, flash, session
import mysql.connector
import random
from functions import *

# Flask app generate
app = Flask(__name__)
app.secret_key = 'secretkey'

# MYSQL database connection
database = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="books"
)
database_cursor = database.cursor()


@app.route("/")
def home():
    searched = False
    return render_template("index.html", searched=searched)


@app.route("/", methods=['POST', 'GET'])
def homeMethods():
    if request.method == "POST":
        searched = True
        search_text = request.form.get("search-text")

        query = "SELECT * FROM book_table WHERE book_name LIKE %s or book_author LIKE %s or book_type LIKE %s"
        values = ("%" + search_text + "%", "%" + search_text + "%", "%" + search_text + "%")
        database_cursor.execute(query, values)
        MatchedBooks = database_cursor.fetchall()

        newIDs = []
        for book in MatchedBooks:
            newIDs.append(generateID(book[0]))

        newData = addIdsToMatchedBooks(MatchedBooks, newIDs)

    return render_template("index.html", matched_books=newData, searched=searched)
    # return str(newData)


@app.route("/random")
def random_template():
    # amount of book categories
    query = "SELECT book_type FROM book_table"
    database_cursor.execute(query, )
    categories = database_cursor.fetchall()
    list_categories = []
    for i in categories:
        list_categories.append(i[0])

    for j in list_categories:
        if list_categories.count(j) > 1:
            list_categories.remove(j)
    return render_template("random.html", all_book_categories=list_categories)


@app.route("/random", methods=["GET", "POST"])
def random_books():
    # generate random book
    random_book_type = request.form.get("select")
    query = "SELECT * FROM book_table WHERE book_type=%s"
    values = (random_book_type,)
    database_cursor.execute(query, values)
    MatchedBooks = database_cursor.fetchall()

    allIds = []
    for book in MatchedBooks:
        allIds.append(book[0])

    randomRange = random.choice(allIds)

    query = "SELECT * FROM book_table WHERE book_id=%s"
    values = (randomRange,)
    database_cursor.execute(query, values)
    RandomBooks = database_cursor.fetchall()

    # amount of book categories
    query = "SELECT book_type FROM book_table"
    database_cursor.execute(query, )
    categories = database_cursor.fetchall()
    list_categories = []
    for i in categories:
        list_categories.append(i[0])

    for j in list_categories:
        if list_categories.count(j) > 1:
            list_categories.remove(j)

    return render_template("random.html", random_books=RandomBooks, all_book_categories=list_categories)
    # return str(list_categories)


@app.route("/admin")
def admin():
    return render_template("admin/admin.html")


@app.route("/admin/add-book")
def add_book_template():
    return render_template("admin/add-book.html")


@app.route("/admin/add-book", methods=["GET", "POST"])
def add_book():
    book_name = request.form.get("book-name")
    book_author = request.form.get("book-author")
    book_type = request.form.get("book-type")
    edition_year = request.form.get("edition-year")
    shelf_number = request.form.get("shelf-number")
    row_number = request.form.get("row-number")
    amount = request.form.get("amount")

    query = "SELECT * FROM book_table WHERE book_name=%s AND book_author=%s AND edition_year=%s"
    values = (book_name, book_author, edition_year)
    database_cursor.execute(query, values)
    existAlready = database_cursor.fetchall()

    if book_name and book_type and book_author and edition_year and shelf_number and row_number and amount != "":
        if not existAlready:
            query = "INSERT INTO book_table (book_name, book_author, book_type, edition_year, shelf_number, row_number, book_amount) VALUES ( %s, %s, %s, %s, %s, %s, %s )"
            values = (book_name, book_author, book_type, edition_year, shelf_number, row_number, amount)
            database_cursor.execute(query, values)
            database.commit()
            flash("Successfully Added!", "Info")
        else:
            flash("Book already exists!", "Error")
    else:
        flash("Fill all information!", "Error")

    return render_template("admin/add-book.html")


@app.route("/admin/delete-book")
def delete_book_template():
    return render_template("admin/delete-book.html")


@app.route("/admin/delete-book", methods=["GET", "POST"])
def delete_book():
    search_text = str(request.form.get("search-text"))
    query = "SELECT * FROM book_table WHERE book_name LIKE %s or book_author LIKE %s or book_type LIKE %s"
    values = ("%" + search_text + "%", "%" + search_text + "%", "%" + search_text + "%")
    database_cursor.execute(query, values)
    MatchedBooks = database_cursor.fetchall()

    newIDs = []
    for book in MatchedBooks:
        newIDs.append(generateID(book[0]))

    newData = addIdsToMatchedBooks(MatchedBooks, newIDs)

    return render_template("admin/delete-book-action.html", matched_books=newData)


@app.route("/admin/delete-book-action", methods=["GET", "POST"])
def delete_book_action():
    book_id = request.form.get("delete-btn")
    query = "DELETE FROM book_table WHERE book_id=%s"
    values = (book_id,)
    database_cursor.execute(query, values)
    database.commit()
    flash("Successfully Deleted!", "Info")

    return render_template("admin/delete-book-action.html")


@app.route("/admin/update-book")
def update_book_template():
    return render_template("admin/update-book.html")


@app.route("/admin/update-book", methods=["GET", "POST"])
def update_book():
    search_text = str(request.form.get("search-text"))
    query = "SELECT * FROM book_table WHERE book_name LIKE %s or book_author LIKE %s or book_type LIKE %s"
    values = ("%" + search_text + "%", "%" + search_text + "%", "%" + search_text + "%")
    database_cursor.execute(query, values)
    MatchedBooks = database_cursor.fetchall()

    return render_template("admin/update-book-choose-book.html", matched_books=MatchedBooks)


@app.route("/admin/update-book-action", methods=["GET", "POST"])
def update_book_action():
    book_id = request.form.get("update-btn")
    query = "SELECT * FROM book_table WHERE book_id=%s"
    values = (book_id,)
    database_cursor.execute(query, values)
    selectedBook = database_cursor.fetchall()

    return render_template("admin/update-book-forms.html", selected_book=selectedBook)


@app.route("/admin/update-book-actions_done", methods=["GET", "POST"])
def update_book_actions_done():
    book_id = request.form.get("book-id")
    book_name = request.form.get("book-name")
    book_author = request.form.get("book-author")
    book_type = request.form.get("book-type")
    edition_year = request.form.get("edition-year")
    shelf_number = request.form.get("shelf-number")
    row_number = request.form.get("row-number")
    amount = request.form.get("amount")

    query = "SELECT * FROM book_table WHERE book_name=%s AND book_author=%s AND edition_year=%s"
    values = (book_name, book_author, edition_year)
    database_cursor.execute(query, values)
    existAlready = database_cursor.fetchall()

    query = """UPDATE book_table 
    SET book_name=%s, 
    book_author=%s, 
    book_type=%s, 
    edition_year=%s, 
    shelf_number=%s, 
    row_number=%s, 
    book_amount=%s
    WHERE book_id=%s
    """
    values = (book_name, book_author, book_type, edition_year, shelf_number, row_number, amount, book_id)
    if not existAlready:
        database_cursor.execute(query, values)
        database.commit()
        flash("Successfully Updated!", "Info")
    else:
        flash("Book Already Exists!", "Error")

    return render_template("admin/update-book-forms.html")


@app.route("/help")
def helps():
    return render_template("help.html")


@app.route("/about")
def about():
    return render_template("about.html")


# Run
app.run(debug=True)
