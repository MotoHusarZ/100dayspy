from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

all_books = [
        {
            "title": "Godfather",
            "author": "Mario Puzo",
            "rating": 9,
        },
        {
            "title": "Fools die",
            "author": "Mario Puzo",
            "rating": 10,
        },
        {
        "title": "Harry Potter",
        "author": "J. K. Rowling", 
        "rating": 9,
    }
        
]

@app.route('/')
def home():
    return render_template("index.html", books=all_books)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = {
            "title": request.form["title"],
            "author": request.form["author"],
            "rating": request.form["rating"]
        }
        all_books.append(new_book)
        #NOTE: You can use the redirect method from flask to redirect to another route 
        # e.g. in this case to the home page after the form has been submitted.
        return redirect(url_for('home'))
    
    return render_template("add.html")

if __name__ == "__main__":
    app.run(debug=True)