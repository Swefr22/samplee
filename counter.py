from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<h1>Counter App</h1>

<h2>{{ count }}</h2>

<form method="POST">

<button name="action" value="increment">
    +
</button>

<button name="action" value="decrement">
    -
</button>

</form>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    count = int(request.args.get("count", 0))

    if request.method == "POST":

        action = request.form["action"]

        if action == "increment":
            count += 1

        elif action == "decrement":
            count -= 1

    return render_template_string(
        HTML,
        count=count
    )

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)