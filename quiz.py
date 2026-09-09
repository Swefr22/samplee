from flask import Flask, request, render_template_string

app = Flask(__name__)

questions = {
    "What is Python?": "language",
    "What is 2 + 2?": "4",
    "What does CPU stand for?": "central processing unit"
}

HTML = """
<h1>Quiz App</h1>

<form method="POST">

{% for question in questions %}
    <p><b>{{ question }}</b></p>
    <input name="{{ question }}" required>
{% endfor %}

<button>Submit Quiz</button>

</form>

<h2>{{ result }}</h2>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    result = ""

    if request.method == "POST":

        score = 0

        for question, answer in questions.items():

            user_answer = request.form[question].lower()

            if user_answer == answer:
                score += 1

        result = f"Score: {score}/{len(questions)}"

    return render_template_string(
        HTML,
        questions=questions,
        result=result
    )

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)