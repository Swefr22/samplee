from flask import Flask, request, render_template_string

app = Flask(__name__)

def algorithm(celsius):
    return (celsius * 9/5) + 32

HTML = """
<h1>Temperature Converter</h1>

<form method="POST">
    <input type="number" step="any" name="temperature"
           placeholder="Celsius" required>
    <button>Convert</button>
</form>

<h2>{{ result }}</h2>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    result = ""

    if request.method == "POST":

        try:
            celsius = float(request.form["temperature"])
            result = f"{algorithm(celsius):.2f} °F"
        except:
            result = "Invalid input"

    return render_template_string(HTML, result=result)

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)