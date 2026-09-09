from flask import Flask, request, render_template_string

app = Flask(__name__)

tasks = []

HTML = """
<h1>To-Do List</h1>

<form method="POST">
    <input name="task" placeholder="Enter task" required>
    <button>Add Task</button>
</form>

<ul>
{% for task in tasks %}
    <li>{{ task }}</li>
{% endfor %}
</ul>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        tasks.append(request.form["task"])

    return render_template_string(HTML, tasks=tasks)

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)