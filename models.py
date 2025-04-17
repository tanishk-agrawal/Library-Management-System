from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()



class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)
    name = db.Column(db.String, nullable = False)
    is_admin = db.Column(db.Boolean, default = False)
    
class Books(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable = False)
    author = db.Column(db.String, nullable = False)
    content = db.Column(db.String)
    added_on = db.Column(db.DateTime, nullable = False)
    price = db.Column(db.Float, nullable = False)
    section_id = db.Column(db.Integer, db.ForeignKey("sections.id"))
    
    borrows = db.relationship('Borrowings', backref = 'book', cascade = 'all, delete')
    bought  = db.relationship('Buys', backref = 'book', cascade = 'all, delete')
    reqst  = db.relationship('Requests', backref = 'book', cascade = 'all, delete')
    reviews = db.relationship('Reviews', backref = 'book', cascade = 'all, delete')
    
class Sections(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable = False)
    description = db.Column(db.String)
    created_on = db.Column(db.DateTime, nullable = False)

    books = db.relationship('Books', backref = 'section', cascade = 'all, delete')
    
class Borrowings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issued_on = db.Column(db.DateTime, nullable = False)
    due_on = db.Column(db.DateTime, nullable = False)
    returned_on = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable = False)

class Buys(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buy_on = db.Column(db.DateTime, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable = False)


class Requests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    no_of_days = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable = False)

class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable = False)
    comment = db.Column(db.String)
    reviewed_on = db.Column(db.DateTime, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable = False)


