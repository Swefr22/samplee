from flask import Flask, request, render_template_string

app = Flask(__name__)

def algorithm(amount, rate):
    return amount * rate

HTML = """
<h1>Currency Converter</h1>

<form method="POST">

<input type="number"
       step="any"
       name="amount"
       placeholder="Amount"
       required>

<input type="number"
       step="any"
       name="rate"
       placeholder="Exchange rate"
       required>

<button>Convert</button>

</form>

<h2>{{ result }}</h2>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    result = ""

    if request.method == "POST":

        try:
            amount = float(request.form["amount"])
            rate = float(request.form["rate"])

            result = f"{algorithm(amount, rate):.2f}"

        except:
            result = "Invalid input"

    return render_template_string(
        HTML,
        result=result
    )

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)