

from flask import Flask, request, redirect, url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
import os
from flask_wtf import FlaskForm #not installed dependcy at the time of learning
from wtforms import StringField, PasswordField, SubmitField #not installed dependcy at the time of learning
from wtforms.validators import DataRequired, Email, Length #not installed dependcy at the time of learning
from flask_bootstrap import Bootstrap #not installed dependcy at the time of learning


# Flask APP - Bootstrap - SQLAlchemy Code Config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection4.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "any-string-you-want-just-keep-it-secret"
Bootstrap(app)
db = SQLAlchemy()
db.init_app(app)


# project_dir = os.path.dirname(os.path.abspath(__file__))
# database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))
#
# app = Flask(__name__)
# CREATE DATABASE
# app.config['SQLALCHEMY_DATABASE_URI'] = database_file
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy()
# db.init_app(app)
class BookForm(FlaskForm):
    book_name = StringField(u'Book Name:', validators=[DataRequired()])
    book_author = StringField(u'Book Author:', validators=[DataRequired()])
    book_rating = StringField(label='Rating', validators=[DataRequired()])
    submit = SubmitField(label="Submit")

class EditForm(FlaskForm):
    new_rating = StringField('New Rating: ', validators=[DataRequired()])
    submit = SubmitField('Submit')

with app.app_context():
    class Book(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(250), unique=True, nullable=False)
        author = db.Column(db.String(250), nullable=False)
        rating = db.Column(db.String(3), nullable=False)

        def __repr__(self):
            return f"Book{self.title}"
    db.create_all()

@app.route('/')
def home():
    global all_books
    all_books = db.session.query(Book).all()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = BookForm()
    if form.validate_on_submit() and request.method == "POST":
        add_book = Book(name=form.book_name.data, author=form.book_author.data,
                         rating=form.book_rating.data)
        db.session.add(add_book)
        db.session.commit()
    # ### Creates form from the class we created above ###
    # form = BookForm()
    #
    # if  form.validate_on_submit() and request.method=="POST":
    #     new_book = Book(title=request.form["title"],
    #                 author = request.form["author"],
    #                 rating = request.form["rating"])
    #     # title = request.form["title"]
    #     # rating = request.form["rating"]
    #     db.session.add(new_book)
    #     db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html", form=form)

@app.route("/edit", methods=["GET", "POST"])
def edit_rating():
    edit_form = EditForm()
    if edit_form.validate_on_submit() and request.method == "POST":
        book_id = request.args.get('id')
        query_to_update = Book.query.get(book_id)
        query_to_update.rating = edit_form.new_rating.data
        db.session.commit()
        print(query_to_update.rating)
        return redirect(url_for('home'))
    # Retrieves the ID from DB with all its values
    book_id = request.args.get('id')
    book_query = Book.query.get(book_id)
    print(book_query)
    return render_template('edit_rating.html', form=edit_form, book=book_query)

    # This is the Second part that's executed when you have changed the rating of the selected
    #  particular book/record from the home page, id of the particular record is passed
    # to this fuction via POST method based on which database is queried and record is updated
    # if request.method == "POST":
    #     # UPDATE RECORD
    #     book_id = request.form["id"]
    #     book_to_update = Book.query.get(book_id)
    #     book_to_update.rating = request.form["rating"]
    #     db.session.commit()
    #     return redirect(url_for('home'))
    # This is the first part that's executed for showing the selected book from the list of books
    # When you select a particular record from the home page, id of the particular record is passed
    # to this fuction based on which database is queried and record is shown for editing rating
    # book_id = request.args.get('id')
    # book_selected = Book.query.get(book_id)
    # return render_template("edit_rating.html", book=book_selected)


@app.route('/delete')
def delete_entry():
    book_id = request.args.get('id')
    query_to_delete = Book.query.get(book_id)
    db.session.delete(query_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
