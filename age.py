from flask import Flask, request, render_template_string

app = Flask(__name__)

def algorithm(year):
    return 2026 - int(year)

HTML = """
<h1>Age Calculator</h1>

<form method="POST">

<input type="number"
       name="year"
       placeholder="Birth year"
       required>

<button>Calculate Age</button>

</form>

<h2>{{ result }}</h2>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    result = ""

    if request.method == "POST":

        try:

            year = int(request.form["year"])

            result = f"Your age is approximately {algorithm(year)} years"

        except:

            result = "Invalid year"

    return render_template_string(
        HTML,
        result=result
    )

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)