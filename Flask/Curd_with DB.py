
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/mydb'
db = SQLAlchemy(app)

class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)

    def __init__(self, title, author):
        super().__init__()
        self.title = title
        self.author = author


    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author
        }       
       

# Create a new book
@app.route('/books', methods=['POST'])
def create_book():
    new_book = Book(request.json['title'], request.json['author'])
    db.session.add(new_book)
    db.session.commit()

    return jsonify({'id': new_book.id, 'title': new_book.title, 'author': new_book.author})

# @app.route('/books', methods=['POST'])
# def create_book():
#     title = request.json.get('title')
#     author = request.json.get('author')

#     new_book = Book(title=title, author=author)
#     db.session.add(new_book)
#     db.session.commit()

#     return jsonify(new_book.to_dict()), 201


# Read all books
@app.route('/books', methods=['GET'])
def get_all_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])

# Read a specific book
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book:
        return jsonify(book.to_dict())
    else:
        return jsonify({"message": "Book not found"}), 404

# Update a book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404

    title = request.json.get('title', book.title)
    author = request.json.get('author', book.author)

    book.title = title
    book.author = author
    db.session.commit()

    return jsonify(book.to_dict())

# Update a specific book
@app.route('/books/<int:book_id>', methods=['PATCH'])
def update_book_author(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404

    # title = request.json.get('title', book.title)
    author = request.json.get('author', book.author)

    # book.title = title
    book.author = author
    db.session.commit()

    return jsonify(book.to_dict())

# Delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404

    db.session.delete(book)
    db.session.commit()

    return jsonify({"message": "Book deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)