from flask import Flask, request, render_template_string

app = Flask(__name__)

books = {
    "python": "Python Crash Course",
    "java": "Head First Java",
    "ai": "Artificial Intelligence: A Modern Approach",
    "data": "Data Science for Beginners"
}

HTML = """
<h1>Book Finder</h1>

<form method="POST">

<input name="book"
       placeholder="Enter book keyword"
       required>

<button>Search</button>

</form>

<h2>{{ result }}</h2>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    result = ""

    if request.method == "POST":

        keyword = request.form["book"].lower()

        result = books.get(
            keyword,
            "Book not found"
        )

    return render_template_string(
        HTML,
        result=result
    )

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)