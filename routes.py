from flask import Flask, request, redirect, render_template, url_for, flash, session, send_file
from app import app
from datetime import date, datetime, timedelta
from models import *
from functools import wraps
from func import *

def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login to continue!!", category="error")
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return inner

def admin_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to continue')
            return redirect(url_for('login'))
        user = Users.query.filter_by(id=session['user_id']).first()
        if not user.is_admin:
            flash('You are not authorized to access this page')
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    return inner


@app.route('/login', methods = ["GET","POST"])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Please fill out all the fields!!", category="error")
            return redirect(url_for('login'))
        
        user = Users.query.filter_by(username = username).first()
        if not user:
            flash("User does not exists!!", category="error")
            return redirect(url_for('login'))
        
        if password != user.password:
            flash("Incorrect password!!", category="error")
            return redirect(url_for('login'))
        
        session['user_id'] = user.id
        flash('Logged in successfully!!')
        return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/register', methods = ["GET","POST"])
def register():
    if 'user_id' in session:
        return redirect(url_for('index'))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        name = request.form.get("name")

        if not username or not password or not name:
            flash("Please fill out all the fields!!", category="error")
            return redirect(url_for('register'))
        
        if Users.query.filter_by(username = username).first():
            flash("User with this username already exists!!", category="error")
            return redirect(url_for('register'))         

        new_user = Users(username=username, password=password, name=name)
        db.session.add(new_user)
        db.session.commit()
        flash('User registered successfully!!')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('user_id')
    return redirect(url_for('login'))

@app.route('/profile/', methods = ["GET","POST"])
@login_required
def profile():
    user = Users.query.filter_by(id = session['user_id']).first()
    
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        npassword = request.form.get("npassword")
        
        if not password or not name:
            flash("Please fill out all the fields!!", category="error")
            return redirect(url_for('profile'))

        if password != user.password:
            flash("Incorrect password!!", category="error")
            return redirect(url_for('profile'))
        
        if npassword:
            user.password=npassword
        user.name=name
        db.session.commit()
    
        flash('Profile Updated Successfully!!')
        return redirect(url_for('profile'))
    
    return render_template('profile.html', user=user, is_admin=user.is_admin)


# -------------Admin Functions-------------
import requests
from generate_graph import *

@app.route('/admin')
@admin_required
def admin():
    r = requests.get('http://localhost:5000/api/stats')
    response=r.json()
    count= response["count"]
    genarate_pie(response["book_per_sec"])
    generate_rating_pareto(response["avg_rating"])
    return render_template('admin.html', count=count, is_admin=True)

@app.route('/manage')
@app.route('/manage/section')
@admin_required
def section():
    sections = Sections.query.all()
    return render_template('section.html', sections=sections, is_admin=True)

@app.route('/manage/section/add', methods=['GET', 'POST'])
@admin_required
def add_section():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")

        if not name:
            flash("Please fill out all the fields!!", category="error")
            return redirect(url_for('add_section'))
        
        if Sections.query.filter_by(name=name).first():
            flash("Section already exists!!", category="error")
            return redirect(url_for('add_section'))      
        
        section = Sections(name=name, description=description, created_on=datetime.now())
        db.session.add(section)
        db.session.commit()
        flash("Section added successfully!!")
        return redirect(url_for('section'))

    return render_template('add_section.html', is_admin=True)

@app.route('/manage/section/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_section(id):
    section = Sections.query.get(id)
    if not section:
        flash("Section does not exists!!", category="error")
        return redirect(url_for('section'))   
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")

        if not name:
            flash("Please fill out all the fields!!", category="error")
            return redirect(url_for('add_section'))
        
        if name!=section.name and Sections.query.filter_by(name=name).first():
            flash("Section already exists!!", category="error")
            return redirect(url_for('add_section'))      
        
        section.name = name
        section.description = description
        db.session.commit()
        flash("Section edited successfully!!")
        return redirect(url_for('section'))

    return render_template('edit_section.html',section=section, is_admin=True)

@app.route('/manage/section/<int:id>/delete', methods=['GET', 'POST'])
@admin_required
def delete_section(id):
    section = Sections.query.get(id)
    if not section:
        flash("Section does not exists!!", category="error")
        return redirect(url_for('section'))

    if request.method == "POST":
        db.session.delete(section)
        db.session.commit()
        flash("Section deleted successfully!!")
        return redirect(url_for('section'))
        
    return render_template('delete_section.html', section=section, is_admin=True)

@app.route('/manage/section/<int:id>')
@admin_required
def view_section(id):
    section = Sections.query.get(id)
    if not section:
        flash("Section does not exsist!!", category="error")
        return redirect(url_for('section'))
    
    books = section.books
    avg_rating=get_avg_rating()
    return render_template('view_section.html', section=section, books=books, avg_rating=avg_rating, is_admin=True)

@app.route('/manage/<int:sec_id>/book/add', methods=['GET', 'POST'])
@admin_required
def add_book(sec_id):
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        price = request.form.get("price")        
        section = request.form.get("section")
        content = request.form.get("content")

        if not title or not author or not price or not section or not content:
            flash("Please fill out all the fields!!", category="error")
            return redirect(url_for('add_book', sec_id=sec_id))
        

        try:
            section = int(section)
            if not Sections.query.get(section):
                raise FileNotFoundError
            price = float(price)
            if price < 1:
                flash("Price should be >1!!", category="error")
                return redirect(url_for('add_book', sec_id=sec_id))
        except:
            flash("Something went wrong!!", category="error")
            return redirect(url_for('add_book', sec_id=sec_id))
                        
        book = Books(title=title, author=author, price=price, section_id=section, content=content, added_on=datetime.now())
        db.session.add(book)
        db.session.commit()
        flash("Book added successfully!!")
        return redirect(url_for('view_section', id=section))
    
    sections = Sections.query.all()
    return render_template('add_book.html', sec_id=sec_id, sections=sections, is_admin=True)

@app.route('/manage/book/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_book(id):
    book = Books.query.get(id)
    if not book:
        flash("Book does not exists!!", category="error")
        return redirect(url_for('section'))
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        price = request.form.get("price")
        section = request.form.get("section")
        content = request.form.get("content")

        if not title or not author or not price or not section or not content:
            flash("Please fill out all the fields!!", category="error")
            return redirect(url_for('edit_book', id=id))
        
        
        try:
            section = int(section)
            price = float(price)
            if price < 1:
                flash("Price should be >1!!", category="error")
                return redirect(url_for('edit_book', id=id))
        except:
            flash("Something went wrong!!", category="error")
            return redirect(url_for('edit_book', id=id))
        
        
        book.title=title
        book.author=author
        book.price=price
        book.section_id=section
        book.content=content
        db.session.commit()
        flash("Book edited successfully!!")
        return redirect(url_for('view_section', id=section))
    
    sections = Sections.query.all()
    return render_template('edit_book.html', book=book, sections=sections, is_admin=True)

@app.route('/manage/book/<int:id>/delete', methods=['GET', 'POST'])
@admin_required
def delete_book(id):
    book = Books.query.get(id)
    if not book:
        flash("Book does not exists!!", category="error")
        return redirect(url_for('section'))
    
    sec_id = book.section_id

    if request.method == "POST":
        db.session.delete(book)
        db.session.commit()
        flash("Book deleted successfully!!")  
        return redirect(url_for('view_section', id=sec_id))
    
    return render_template('delete_book.html', book=book, is_admin=True)

@app.route('/manage/book/<int:id>')
@admin_required
def view_book(id):
    book = Books.query.get(id)
    if not book:
        flash("Book does not exists!!", category="error")
        return redirect(url_for('section'))
    borrows = Borrowings.query.filter_by(book_id=id, returned_on=None).all()
    return render_template('view_book.html', book=book, borrows=borrows, username=get_usernames(), is_admin=True)

@app.route('/manage/review/<int:id>/delete')
@admin_required
def remove_review(id):
    review = Reviews.query.get(id)
    if not review:
        return redirect(url_for('view_book', id=review.book_id))
    db.session.delete(review)
    db.session.commit()
    flash('Review deleted successfully!!')
    return redirect(url_for('view_book', id=review.book_id))

@app.route('/requests', methods=['GET', 'POST'])
@admin_required
def manage_requests():
    req = Requests.query.all()
    borrows = Borrowings.query.filter_by(returned_on=None).all()
    buys = Buys.query.all()
    username = get_usernames()
    return render_template('manage_request.html', req=req, borrows=borrows, buys=buys, username=username, is_admin=True)    

@app.route('/requests/<int:id>/grant', methods=['POST'])
@admin_required
def grant_request(id):
    req = Requests.query.get(id)
    if not req:
        return redirect(url_for('admin'))
    
    days=request.form.get('days')
    try:
        days=int(days)
    except:
        return redirect(url_for('manage_requests'))

    issued_on=datetime.now()
    due_on = issued_on + timedelta(days=days)
    borrow = Borrowings(user_id=req.user_id, book_id=req.book_id, issued_on=issued_on, due_on=due_on)
    db.session.add(borrow)
    db.session.delete(req)
    db.session.commit()
    return redirect(url_for('manage_requests'))

@app.route('/requests/<int:id>/reject')
@admin_required
def reject_request(id):
    req = Requests.query.get(id)
    if not req:
        return redirect(url_for('admin'))
    db.session.delete(req)
    db.session.commit()
    return redirect(url_for('manage_requests'))

@app.route('/borrowings/<int:id>/revoke')
@admin_required
def revoke_borrow(id):
    borrow = Borrowings.query.get(id)
    if not borrow:
        return redirect(url_for('admin'))
    borrow.returned_on = datetime.now()
    db.session.commit()
    return redirect(url_for('manage_requests'))


# -------------User Functions-------------
@app.route('/')
@login_required
def index():
    user = Users.query.get(session['user_id'])
    if not user:
        return redirect(url_for('logout'))
    if user.is_admin:
        return redirect(url_for('admin'))
    srch_filter =  {1:'Book', 2:'Section', 3:'Author'}
    books = Books.query.order_by(Books.added_on.desc()).all()
    sections = Sections.query.all()
    avg_rating=get_avg_rating()
    return render_template('index.html', books=books, sections=sections, srch_filter=srch_filter, avg_rating=avg_rating, user=user)

@app.route('/search')
@login_required
def search():
    user = Users.query.get(session['user_id'])
    srch_filter =  {'1':'Book', '2':'Section', '3':'Author'}
    srch_args = {}
    try:
        srch_args['filter'] = request.args.get("filter")
        srch_args['value'] = request.args.get("value").strip()
    except:
        flash("Something went wrong!!", category="error")
        return redirect(url_for('index'))
    
    books = Books.query.all()
    if srch_args['value']=='':
        pass
    elif srch_args['filter'] == '1':
        books = Books.query.filter(Books.title.ilike(f'%{srch_args["value"]}%')).all()
    elif srch_args['filter'] == '2':
        sections = Sections.query.filter(Sections.name.ilike(f'%{srch_args["value"]}%')).all()
        books=[]
        for section in sections:
            books += section.books
        books = set(books)
    elif srch_args['filter'] == '3':
        books = Books.query.filter(Books.author.ilike(f'%{srch_args["value"]}%')).all()

    return render_template('search.html',books=books, srch_args=srch_args, srch_filter=srch_filter, avg_rating=get_avg_rating())


@app.route('/mybooks')
@login_required
def user_books():
    user = Users.query.get(session['user_id'])
    if user.is_admin:
        return redirect(url_for('admin'))
    check_book_due()
    buys = Buys.query.filter_by(user_id=session['user_id']).all()
    reqsts = Requests.query.filter_by(user_id=session['user_id']).all()
    curr_borrows = Borrowings.query.filter_by(user_id=session['user_id'], returned_on=None).all()
    past_borrows = get_past_books()
    return render_template('mybooks.html', curr_borrows=curr_borrows, past_borrows=past_borrows, buys=buys, reqsts=reqsts, user=user, avg_rating=get_avg_rating())



@app.route('/book/<int:id>')
@login_required
def show_book(id):
    user = Users.query.get(session['user_id'])
    book = Books.query.get(id)
    if not book:
        flash("Book does not exists!!", category="error")
        return redirect(url_for('index'))
    check_book_due()
    avg_rating=get_avg_rating()
    username=get_usernames()
    buy = Buys.query.filter_by(book_id=id, user_id=session['user_id']).first()
    borrow = Borrowings.query.filter_by(book_id=id, user_id=session['user_id'], returned_on=None).first()
    reqst = Requests.query.filter_by(book_id=id, user_id=session['user_id']).first()
    return render_template('show_book.html', book=book, borrow=borrow, buy=buy, reqst=reqst, avg_rating=avg_rating, username=username, user=user)

@app.route('/book/<int:id>/review', methods=['GET', 'POST'])
@login_required
def review_book(id):
    user = Users.query.get(session['user_id'])
    book = Books.query.get(id)
    if not book:
        flash("Book does not exists!!", category="error")
        return redirect(url_for('index'))
    if request.method == "POST":
        rating = request.form.get("rating")
        comment = request.form.get("comment")

        if not rating or not comment:
            flash("Please fill out all the fields!!", category="error")
            return redirect(url_for('review_book'))        
        try:
            rating = int(rating)
        except:
            return redirect(url_for('review_book'))
        
        review= Reviews(book_id=id, user_id=session['user_id'], rating=rating, comment=comment, reviewed_on=datetime.now())
        db.session.add(review)
        db.session.commit()
        flash("Book reviewed successfully!!")
        return redirect(url_for('show_book', id=id))
    return render_template('add_review.html', book=book)

@app.route('/book/<int:id>/request', methods=['GET', 'POST'])
@login_required
def request_book(id):
    user = Users.query.get(session['user_id'])
    if user_book_limit() >= 5:
        flash('You have reached limit (max no. of books=5)', category='error')
        return redirect(url_for('show_book', id=id))    

    req = Requests.query.filter_by(user_id=session['user_id'], book_id=id).first()
    if req:
        return redirect(url_for('show_book', id=id))
    
    if request.method == "POST":
        no_of_days = request.form.get("days")
        req = Requests(user_id=session['user_id'], book_id=id, no_of_days=no_of_days)
        db.session.add(req)
        db.session.commit()
        return redirect(url_for('show_book', id=id))
    
    book = Books.query.get(id)
    if not book:
        flash("Book does not exists!!", category="error")
        return redirect(url_for('index'))
    return render_template('request.html', book=book, user=user)

@app.route('/book/<int:id>/request/delete')
@login_required
def request_delete(id):
    req = Requests.query.filter_by(user_id=session['user_id'], book_id=id).first()
    if req:
        db.session.delete(req)
        db.session.commit()
    return redirect(url_for('show_book', id=id))

@app.route('/book/<int:id>/return')
@login_required
def return_book(id):
    borrow = Borrowings.query.filter_by(user_id=session['user_id'], book_id=id, returned_on=None).first()
    if not borrow:
        return redirect(url_for('show_book', id=id))
    borrow.returned_on = datetime.now()
    db.session.commit()
    flash('Book returned successfully!!')
    return redirect(url_for('show_book', id=id))

@app.route('/book/<int:id>/buy', methods=['GET', 'POST'])
@login_required
def buy_book(id):
    user = Users.query.get(session['user_id'])
    book = Books.query.get(id)
    if not book:
        flash("Book does not exists!!", category="error")
        return redirect(url_for('index'))

    if request.method == "POST":
        buy = Buys(user_id=session['user_id'], book_id=id, buy_on=datetime.now())
        db.session.add(buy)

        req = Requests.query.filter_by(user_id=session['user_id'], book_id=id).first()
        borrow = Borrowings.query.filter_by(user_id=session['user_id'], book_id=id, returned_on=None).all()
        if req:
            db.session.delete(req)
        if len(borrow)>0:
            for x in borrow:
                x.returned_on=datetime.now()

        db.session.commit()
        return redirect(url_for('show_book', id=id))

    return render_template('buy.html', book=book, user=user)

@app.route('/book/<int:id>/download')
@login_required
def download_book(id):
    buy = Buys.query.filter_by(user_id=session['user_id'], book_id=id)
    if not buy:
        flash('You are not allowed to download this book', category='error')
        return redirect(url_for('show_book', id=id))

    book = Books.query.get(id)
    if not book:
        flash("Book does not exists!!", category="error")
        return redirect(url_for('index'))
    
    try:
        create_pdf(book)
        return send_file("static/book.pdf", as_attachment=True, download_name=f'{book.title}.pdf')
    except:
        flash("Unable to download", category="error")
        return redirect(url_for('show_book', id=id))

@app.route('/book/<int:id>/read')
@login_required
def read_book(id):
    check_book_due()
    buy = Buys.query.filter_by(user_id=session['user_id'], book_id=id).first()
    borrow = Borrowings.query.filter_by(user_id=session['user_id'], book_id=id, returned_on=None).first()
    if not buy and not borrow:
        flash('You are not allowed to read this book', category='error')
        return redirect(url_for('show_book', id=id))

    book = Books.query.get(id)
    if not book:
        flash("Book does not exists!!", category="error")
        return redirect(url_for('index'))
    
    txt= readBook(book.content)
    return render_template('read_book.html', book=book, txt=txt)

