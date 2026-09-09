from flask import Flask, request, render_template_string

app = Flask(__name__)


def algorithm(a, b):
    """
    Write your main logic here.
    Change only this function for different questions.
    """
    return a + b


HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>

    <style>
        body {
            font-family: Arial;
            background: #f2f2f2;
            text-align: center;
        }

        .container {
            width: 450px;
            margin: 80px auto;
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 0 10px #ccc;
        }

        input {
            width: 90%;
            padding: 12px;
            margin: 8px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }

        button {
            padding: 12px 25px;
            margin: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        .result {
            margin-top: 20px;
            padding: 15px;
            background: #eeeeee;
            border-radius: 5px;
        }

        .error {
            color: red;
        }
    </style>
</head>

<body>

<div class="container">

    <h1>{{ title }}</h1>

    <form method="POST">

        <input
            type="number"
            name="input1"
            placeholder="Enter first value"
            required
        >

        <input
            type="number"
            name="input2"
            placeholder="Enter second value"
            required
        >

        <button type="submit">
            Calculate
        </button>

    </form>

    {% if result != "" %}

        <div class="result">
            <h2>Result</h2>
            <p>{{ result }}</p>
        </div>

    {% endif %}

</div>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():

    result = ""

    if request.method == "POST":

        try:
            a = float(request.form["input1"])
            b = float(request.form["input2"])

            result = algorithm(a, b)

        except Exception:
            result = "Invalid input"

    return render_template_string(
        HTML,
        title="My Application",
        result=result
    )


@app.route("/health")
def health():

    return "OK"


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )