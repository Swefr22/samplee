from flask import Flask, request, render_template_string

app = Flask(__name__)

expenses = []

HTML = """
<h1>Expense Tracker</h1>

<form method="POST">

    <input name="item" placeholder="Expense name" required>

    <input type="number" step="any"
           name="amount"
           placeholder="Amount"
           required>

    <button>Add Expense</button>

</form>

{% for expense in expenses %}
    <p>{{ expense.item }} - ₹{{ expense.amount }}</p>
{% endfor %}

<h2>Total: ₹{{ total }}</h2>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        item = request.form["item"]
        amount = float(request.form["amount"])

        expenses.append({
            "item": item,
            "amount": amount
        })

    total = sum(e["amount"] for e in expenses)

    return render_template_string(
        HTML,
        expenses=expenses,
        total=total
    )

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)