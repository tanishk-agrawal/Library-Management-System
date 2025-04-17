from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library_app_db.sqlite3"
app.secret_key = "mysecretkey"

db.init_app(app)
app.app_context().push()
db.create_all()
librarian = Users.query.filter_by(is_admin = True).first()
if not librarian:
    librarian = Users(username='admin', password='admin', name='Librarian', is_admin=True)
    db.session.add(librarian)
    db.session.commit()

import api
import stats_api
from routes import *

if __name__ == "__main__":
    app.run(debug=True)
