from flask import Flask, render_template_string

app = Flask(__name__)

news = [
    "AI technology continues to grow",
    "Cloud computing adoption increases",
    "New developments in machine learning"
]

HTML = """
<h1>News App</h1>

{% for article in news %}
    <div>
        <h3>{{ article }}</h3>
    </div>
{% endfor %}
"""

@app.route("/")
def home():
    return render_template_string(HTML, news=news)

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)