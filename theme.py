from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>

<head>

<title>Theme Switcher</title>

<style>

body {
    font-family: Arial;
    text-align: center;
    padding: 100px;
    transition: 0.3s;
}

.dark {
    background: #222;
    color: white;
}

.light {
    background: white;
    color: black;
}

button {
    padding: 15px;
}

</style>

</head>

<body class="light" id="page">

<h1>Dark / Light Theme</h1>

<button onclick="changeTheme()">
    Switch Theme
</button>

<script>

function changeTheme() {

    let page = document.getElementById("page");

    if (page.className === "light") {
        page.className = "dark";
    } else {
        page.className = "light";
    }

}

</script>

</body>

</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)