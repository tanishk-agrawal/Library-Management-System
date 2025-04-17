from flask_restful import Resource, Api
from app import app
from models import *

api = Api(app)

def count_stats():
    count={}
    user = Users.query.filter_by(is_admin=False).all()
    count["Users"]=len(user)
    books= Books.query.all()
    count["Books"]=len(books)
    req = Requests.query.all()
    count["Requests"]=len(req)
    borrow = Borrowings.query.filter_by(returned_on=None).all()
    count["Borrows"]=len(borrow)
    return count

def books_per_section():
    book_per_sec={}
    sec = Sections.query.all()
    for item in sec:
        book_per_sec[item.name]=len(item.books)
    return book_per_sec

def book_rating():
    books = Books.query.all()
    b_rating={}
    for item in books:
        if item.section.name in b_rating:
            b_rating[item.section.name]+=item.reviews
        else:
            b_rating[item.section.name]=item.reviews
    avg_rating={}
    for item in b_rating:
        rating_list = [x.rating for x in b_rating[item]]
        try:
            avg_rating[item]= round((sum(rating_list)/len(rating_list)), 1)
        except:
            avg_rating[item]= 0
    return avg_rating

class StatsAPI(Resource):
    def get(self):
        try:
            count=count_stats()
            book_per_sec=books_per_section()
            avg_rating=book_rating()
            return {
                "count":count,
                "book_per_sec":book_per_sec,
                "avg_rating":avg_rating
            }, 200
        except:
            return "Internal Server Error", 500
        
api.add_resource(StatsAPI, '/api/stats')
