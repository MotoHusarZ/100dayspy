from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#solution from here: https://gist.github.com/angelabauer/d7af893cdd72311d674d709421fa389d

app = Flask(__name__)

##CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collections.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CREATE TABLE
with app.app_context():
    class books(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(250), unique=True, nullable=False)
        author = db.Column(db.String(250), nullable=False)
        rating = db.Column(db.String(250), nullable=False)

        def __repr__(self):
            return '<books %r>' % self.title

#CREATE RECORD
    db.create_all()
    new_book = books(id=1, title="Harry Potter", author="J. K. Rowling", rating=9.3)
    db.session.add(new_book)
    db.session.commit()