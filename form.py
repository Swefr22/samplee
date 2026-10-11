
from flask import Flask, request, jsonify, render_template_string
import re
import os

app = Flask(__name__)

PAGE = """
<!DOCTYPE html><html><head><title>Form Validation</title>
<style>
body{font-family:Arial;background:#edf7f1;display:grid;place-items:center;min-height:90vh}
main{background:white;padding:28px;border-radius:15px;width:min(400px,85vw)}
input,button{box-sizing:border-box;width:100%;padding:12px;margin:8px 0;border-radius:8px}
input{border:1px solid #bbb}button{background:#137547;color:white;border:0;cursor:pointer}
#message{white-space:pre-line}
</style></head><body><main><h1>Registration Form</h1>
<form id="form">
<label>Name</label><input name="name" placeholder="Your name" required>
<label>Email</label><input name="email" type="email" placeholder="you@example.com" required>
<label>Age</label><input name="age" type="number" min="1" max="120" required>
<button type="submit">Validate</button>
</form><p id="message"></p>
<script>
document.getElementById('form').addEventListener('submit',async e=>{
 e.preventDefault();
 const form=e.currentTarget;
 const data=Object.fromEntries(new FormData(form).entries());
 const response=await fetch('/api/validate',{
   method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)
 });
 const result=await response.json();
 document.getElementById('message').textContent=response.ok?
   result.message:'Please fix:\\n'+result.errors.join('\\n');
});
</script></main></body></html>
"""

def validate(data):
    errors = []
    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip()
    age = str(data.get("age", "")).strip()

    if len(name) < 2:
        errors.append("Name must contain at least 2 characters.")
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        errors.append("Enter a valid email address.")
    try:
        number = int(age)
        if not 1 <= number <= 120:
            errors.append("Age must be between 1 and 120.")
    except ValueError:
        errors.append("Age must be a whole number.")

    return errors

@app.get("/")
def home():
    return render_template_string(PAGE)

@app.get("/api/health")
def health():
    return jsonify(status="ok")

@app.post("/api/validate")
def validate_form():
    data = request.get_json(silent=True) or {}
    errors = validate(data)
    if errors:
        return jsonify(valid=False, errors=errors), 400
    return jsonify(valid=True, message="Form submitted successfully!")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
