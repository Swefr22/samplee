from flask import Flask, request, render_template_string

app = Flask(__name__)

notes = []

HTML = """
<h1>Notes App</h1>

<form method="POST">
    <textarea name="note" placeholder="Enter your note" required></textarea>
    <br>
    <button>Add Note</button>
</form>

<h2>Notes</h2>

<ul>
{% for note in notes %}
    <li>{{ note }}</li>
{% endfor %}
</ul>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        notes.append(request.form["note"])

    return render_template_string(HTML, notes=notes)

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)