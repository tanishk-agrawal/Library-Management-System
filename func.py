from flask import Flask, session
from datetime import date, datetime, timedelta
from fpdf import FPDF
from models import *

def get_usernames():
    users = Users.query.all()
    username = {}
    for user in users:
        username[user.id] = user.username
    return username

def check_book_due():
    borrow = Borrowings.query.filter_by(returned_on=None).all()
    for item in borrow:
        if item.due_on <= datetime.now():
            item.returned_on = datetime.now()
            db.session.commit()
    return

def user_book_limit():
    req = Requests.query.filter_by(user_id=session['user_id']).all()
    borrow = Borrowings.query.filter_by(user_id=session['user_id'], returned_on=None).all()
    n = len(req)+len(borrow)
    return n

def get_past_books():
    borrows = Borrowings.query.filter_by(user_id=session['user_id']).all()
    buys = Buys.query.filter_by(user_id=session['user_id']).all()
    curr_borrows = Borrowings.query.filter_by(user_id=session['user_id'],returned_on=None).all()
    curr_books = set( [x.book for x in curr_borrows])
    all_books = set([x.book for x in borrows ])
    buy_books = set([x.book for x in buys])
    past_books = all_books.difference(curr_books.union(buy_books))
    return past_books

def get_avg_rating():
    reviews = Reviews.query.all()
    rating_book = {}
    for x in reviews:
        if x.book_id in rating_book.keys():
            rating_book[x.book_id].append(x.rating)
        else:
            rating_book[x.book_id]= [x.rating]

    avg_rating = {}
    for x in rating_book.keys():
        avg_rating[x] = round((sum(rating_book[x])/len(rating_book[x])), 1)

    return avg_rating

def readBook(text):
    text = text.replace('\n', '<br>')
    return text

def create_pdf(book):
    pdf = FPDF(orientation='P', unit='mm', format='A4')

    pdf.add_page()
    pdf.set_y(100)
    pdf.set_font(family='Times', style='B', size=40)
    pdf.multi_cell(w=0, h=20, txt=book.title, align='C')    
    pdf.set_font(family='Times', style='I', size=20)
    pdf.multi_cell(w=0, h=5, txt=f"by {book.author}", align='C')

    pdf.add_page()
    pdf.set_font(family='Times', size=18)
    text=book.content.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(w=0, h=8, txt=text)
    pdf.output("static/book.pdf")