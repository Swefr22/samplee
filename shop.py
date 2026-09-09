from flask import Flask, request, render_template_string

app = Flask(__name__)

def algorithm(price, quantity):

    return price * quantity

HTML = """
<h1>Online Shopping</h1>

<form method="POST">

<input type="number"
       step="any"
       name="price"
       placeholder="Product price"
       required>

<input type="number"
       name="quantity"
       placeholder="Quantity"
       required>

<button>Calculate Total</button>

</form>

<h2>{{ result }}</h2>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    result = ""

    if request.method == "POST":

        try:

            price = float(request.form["price"])
            quantity = int(request.form["quantity"])

            result = f"Total: ₹{algorithm(price, quantity):.2f}"

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