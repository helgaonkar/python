from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/mydb'
db = SQLAlchemy(app)

# Sample data
books = [
    {"id": 1, "title": "Book 1", "author": "Author 1"},
    {"id": 2, "title": "Book 2", "author": "Author 2"}
]


class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)


def __init__(self, title, author):
    self.title = title
    self.author = author


# Read all books
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(Book)


# Read a specific book
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    for book in books:
        if book['id'] == book_id:
            return jsonify(book)

    return jsonify({"message": "Book not found"})


# Create a new book
@app.route('/books', methods=['POST'])
def create_book():
    new_book = {
        "id": len(Book.length) + 1,
        "title": request.json.title,
        "author": request.json.author
    }
    books.append(new_book)

    return jsonify(new_book)


# Update a book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    for book in books:
        if book['id'] == book_id:
            book['title'] = request.json.get('title', book['title'])
            book['author'] = request.json.get('author', book['author'])
            return jsonify(book)

    return jsonify({"message": "Book not found"})


# Update author of book
@app.route('/books/<int:book_id>', methods=['PATCH'])
def update_authorofbook(book_id):
    for book in books:
        if book['id'] == book_id:
            book['author'] = request.json.get('author', book['author'])
            return jsonify(book)
    return jsonify({"message": "Book not found"})


# Delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return jsonify({"message": "Book deleted"})

    return jsonify({"message": "Book not found"})


if __name__ == '__main__':
    app.run(debug=True)
