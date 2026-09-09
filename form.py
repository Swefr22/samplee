from flask import Flask, request, render_template_string

app = Flask(__name__)

def validate(username, password):

    if username == "":
        return "Username is required"

    if len(password) < 6:
        return "Password must contain at least 6 characters"

    return "Login successful"

HTML = """
<h1>Form Validation</h1>

<form method="POST">

<input name="username"
       placeholder="Username"
       required>

<input type="password"
       name="password"
       placeholder="Password"
       required>

<button>Login</button>

</form>

<h2>{{ result }}</h2>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    result = ""

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        result = validate(
            username,
            password
        )

    return render_template_string(
        HTML,
        result=result
    )

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)