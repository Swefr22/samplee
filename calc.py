from flask import Flask, request, render_template_string

app = Flask(__name__)

def algorithm(a, b, operation):
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            return "Cannot divide by zero"
        return a / b

HTML = """
<h1>Calculator</h1>

<form method="POST">
    <input type="number" step="any" name="a" placeholder="First number" required>
    <input type="number" step="any" name="b" placeholder="Second number" required>

    <select name="operation">
        <option value="add">Add</option>
        <option value="subtract">Subtract</option>
        <option value="multiply">Multiply</option>
        <option value="divide">Divide</option>
    </select>

    <button>Calculate</button>
</form>

<h2>{{ result }}</h2>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""

    if request.method == "POST":
        try:
            a = float(request.form["a"])
            b = float(request.form["b"])
            operation = request.form["operation"]
            result = algorithm(a, b, operation)
        except:
            result = "Invalid input"

    return render_template_string(HTML, result=result)

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)