from flask import Flask, request, render_template_string

app = Flask(__name__)

def algorithm(weight, height):

    bmi = weight / (height * height)

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    return f"BMI: {bmi:.2f} - {category}"

HTML = """
<h1>BMI Calculator</h1>

<form method="POST">

<input type="number" step="any"
       name="weight"
       placeholder="Weight (kg)"
       required>

<input type="number" step="any"
       name="height"
       placeholder="Height (m)"
       required>

<button>Calculate BMI</button>

</form>

<h2>{{ result }}</h2>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    result = ""

    if request.method == "POST":

        try:
            weight = float(request.form["weight"])
            height = float(request.form["height"])

            if height <= 0:
                raise ValueError

            result = algorithm(weight, height)

        except:
            result = "Invalid input"

    return render_template_string(HTML, result=result)

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)