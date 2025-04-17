from flask_restful import Resource, Api, reqparse
from app import app
from models import *
from datetime import datetime

api = Api(app)

def get_section_output(section):    
    return  {
        "section_id": section.id,
        "section_name": section.name,
        "section_date_created": section.created_on.strftime("%d-%m-%Y, %H:%M:%S.%f"),
        "section_description": section.description
    }

section_parser = reqparse.RequestParser()
section_parser.add_argument('section_name')
section_parser.add_argument('section_description')

class SectionAPI(Resource):
    def get(self, section_id=None):
        try:
            if not section_id:
                sections=Sections.query.all()
                if len(sections)>0:
                    return [get_section_output(section) for section in sections], 200
                else:
                    return "No Sections found", 404
            
            section=Sections.query.get(section_id)
            if section:
                return get_section_output(section), 200
            else:
                return "Section not found", 404
        except: 
            return "Internal Server Error", 500
    
    def post(self):
        try:
            args = section_parser.parse_args()
            section_name = args.get("section_name")
            section_description = args.get("section_description")

            if not section_name:
                return "Section Name is required", 400
            if Sections.query.filter_by(name=section_name).first():
                return "Section already exists", 409

            section = Sections(name=section_name,
                                description=section_description,
                                created_on=datetime.now())
            db.session.add(section)
            db.session.commit()
            return get_section_output(section), 201
        except:
            return "Internal Server Error", 500
        
    def put(self, section_id):
        try:
            section=Sections.query.get(section_id)
            if not section:
                return "Section not found", 404
            
            args = section_parser.parse_args()
            section_name = args.get("section_name")
            section_description = args.get("section_description")

            if not section_name:
                return "Section Name is required", 400
            if section.name!=section_name and Sections.query.filter_by(name=section_name).first():
                return "Section already exists", 409

            section.name=section_name
            section.description=section_description
            db.session.commit()
            return get_section_output(section), 200
        except:
            return "Internal Server Error", 500
        
    def delete(self, section_id):
        try:
            section=Sections.query.get(section_id)
            if not section:
                return "Section not found", 404
            db.session.delete(section)
            db.session.commit()
            return "Section Deleted Successfully", 200
        except:
            return "Internal Server Error", 500
        

def get_book_output(book):    
    return  {
        "book_id": book.id,
        "book_title": book.title,
        "book_author": book.author,
        "book_section_id": book.section_id,
        "book_price": book.price,
        "book_date_added": book.added_on.strftime("%d-%m-%Y, %H:%M:%S.%f"),
        "book_content": book.content
    }

book_parser = reqparse.RequestParser()
book_parser.add_argument('book_title')
book_parser.add_argument('book_author')
book_parser.add_argument('book_section_id')
book_parser.add_argument('book_price')
book_parser.add_argument('book_content')

class BookAPI(Resource):
    def get(self, book_id=None):
        try:
            if not book_id:
                books=Books.query.all()
                if len(books)>0:
                    return [get_book_output(book) for book in books], 200
                else:
                    return "No Books found", 404
            
            book=Books.query.get(book_id)
            if book:
                return get_book_output(book), 200
            else:
                return "Book not found", 404
        except:
            return "Internal Server Error", 500

    def post(self):
        try:
            args = book_parser.parse_args()
            book_title = args.get("book_title")
            book_author = args.get("book_author")
            book_section_id = args.get("book_section_id")
            book_price = args.get("book_price")
            book_content = args.get("book_content")

            if not book_title:
                return "Book Title is required", 400
            if not book_author:
                return "Book Author is required", 400
            if not book_section_id:
                return "Section ID is required", 400
            if not book_price:
                return "Book Price is required", 400
            if not book_content:
                return "Book Content is required", 400

            try:
                book_section_id = int(book_section_id)
            except:
                return "Invalid Section ID", 400
            if not Sections.query.get(book_section_id):
                return "Section not found", 404
            
            try:
                book_price = float(book_price)
            except:
                return "Invalid Book Price", 400
            if book_price<1:
                return "Book Price must be >1", 400
            
            book = Books(title=book_title, 
                         author=book_author, 
                         price=book_price, 
                         section_id=book_section_id, 
                         content=book_content, 
                         added_on=datetime.now())
            db.session.add(book)
            db.session.commit()
            return get_book_output(book), 201
        except:
            return "Internal Server Error", 500
        
    def put(self, book_id):
        try:
            book = Books.query.get(book_id)
            if not book:
                return "Book not found", 404
            
            args = book_parser.parse_args()
            book_title = args.get("book_title")
            book_author = args.get("book_author")
            book_section_id = args.get("book_section_id")
            book_price = args.get("book_price")
            book_content = args.get("book_content")

            if not book_title:
                return "Book Title is required", 400
            if not book_author:
                return "Book Author is required", 400
            if not book_section_id:
                return "Section ID is required", 400
            if not book_price:
                return "Book Price is required", 400
            if not book_content:
                return "Book Content is required", 400

            try:
                book_section_id = int(book_section_id)
            except:
                return "Invalid Section ID", 400
            if not Sections.query.get(book_section_id):
                return "Section not found", 404
            
            try:
                book_price = float(book_price)
            except:
                return "Invalid Book Price", 400
            if book_price<1:
                return "Book Price must be >1", 400
            
            book.title=book_title 
            book.author=book_author 
            book.price=book_price 
            book.section_id=book_section_id 
            book.content=book_content
            db.session.commit()
            return get_book_output(book), 200
        except:
            return "Internal Server Error", 500
        
    def delete(self, book_id):
        try:
            book=Books.query.get(book_id)
            if not book:
                return "Book not found", 404
            db.session.delete(book)
            db.session.commit()
            return "Book Deleted Successfully", 200
        except:
            return "Internal Server Error", 500




api.add_resource(SectionAPI, '/api/section', '/api/section/<int:section_id>')
api.add_resource(BookAPI, '/api/book', '/api/book/<int:book_id>')
