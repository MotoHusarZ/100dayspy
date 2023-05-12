from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#solution from here: https://gist.github.com/angelabauer/d7af893cdd72311d674d709421fa389d

app = Flask(__name__)
app.app_context().push() #need to add this line to make it work
# YOU NEED to add SQL connection code above to make below work, or maybe even some fixes are needed, not tested yet.
# https://www.udemy.com/course/100-days-of-code/learn/lecture/22591302#questions/18398486
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Read All Records
class Book(db.Model): #something NEED TO BE FIXED HERE:
    
    #Read A Particular Record By Query
    book = Book.query.filter_by(title="Harry Potter").first()


    #Update A Particular Record By Query
    book_to_update = Book.query.filter_by(title="Harry Potter").first()
    book_to_update.title = "Harry Potter and the Chamber of Secrets"
    db.session.commit()  


    #Update A Record By PRIMARY KEY
    book_id = 1
    book_to_update = Book.query.get(book_id)
    book_to_update.title = "Harry Potter and the Goblet of Fire"
    db.session.commit()  


    #Delete A Particular Record By PRIMARY KEY
    book_id = 1
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
#You can also delete by querying for a particular value e.g. by title or one of the other properties.