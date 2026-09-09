from flask import Flask, request, render_template_string

app = Flask(__name__)

dictionary = {
    "python": "A programming language",
    "algorithm": "A step-by-step procedure",
    "database": "An organized collection of data",
    "cloud": "Internet-based computing services"
}

HTML = """
<h1>Dictionary App</h1>

<form method="POST">

<input name="word"
       placeholder="Enter a word"
       required>

<button>Search</button>

</form>

<h2>{{ result }}</h2>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    result = ""

    if request.method == "POST":

        word = request.form["word"].lower()

        result = dictionary.get(
            word,
            "Word not found"
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