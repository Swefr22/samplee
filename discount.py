from flask import Flask, request, render_template_string

app = Flask(__name__)

def algorithm(price, discount):

    discount_amount = price * discount / 100

    final_price = price - discount_amount

    return final_price

HTML = """
<h1>Discount Calculator</h1>

<form method="POST">

<input type="number"
       step="any"
       name="price"
       placeholder="Original price"
       required>

<input type="number"
       step="any"
       name="discount"
       placeholder="Discount %"
       required>

<button>Calculate</button>

</form>

<h2>{{ result }}</h2>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    result = ""

    if request.method == "POST":

        try:

            price = float(request.form["price"])
            discount = float(request.form["discount"])

            result = f"Final Price: ₹{algorithm(price, discount):.2f}"

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