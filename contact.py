from flask import Flask, request, render_template_string

app = Flask(__name__)

contacts = {}

HTML = """
<h1>Contact Book</h1>

<form method="POST">

<input name="name" placeholder="Name" required>
<input name="phone" placeholder="Phone" required>

<button>Add Contact</button>

</form>

<h2>Contacts</h2>

{% for name, phone in contacts.items() %}
<p>{{ name }} : {{ phone }}</p>
{% endfor %}
"""

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]

        contacts[name] = phone

    return render_template_string(
        HTML,
        contacts=contacts
    )

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)