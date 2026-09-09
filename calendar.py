from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<h1>Calendar Picker</h1>

<form method="POST">

<input type="date"
       name="date"
       required>

<button>Select Date</button>

</form>

<h2>{{ result }}</h2>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    result = ""

    if request.method == "POST":

        result = "Selected date: " + request.form["date"]

    return render_template_string(
        HTML,
        result=result
    )

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)