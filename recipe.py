from flask import Flask, request, render_template_string

app = Flask(__name__)

recipes = {
    "pasta": "Pasta, tomato sauce, garlic and cheese",
    "pizza": "Flour, tomato sauce, cheese and vegetables",
    "sandwich": "Bread, vegetables and cheese"
}

HTML = """
<h1>Recipe Finder</h1>

<form method="POST">

<input name="recipe"
       placeholder="Enter recipe"
       required>

<button>Search</button>

</form>

<h2>{{ result }}</h2>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    result = ""

    if request.method == "POST":

        recipe = request.form["recipe"].lower()

        result = recipes.get(
            recipe,
            "Recipe not found"
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