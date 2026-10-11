
from flask import Flask, jsonify, request, render_template_string
import os

app = Flask(__name__)

PAGE = """
<!DOCTYPE html><html><head><title>BMI Calculator</title>
<meta name="viewport" content="width=device-width">
<style>
body{font:18px Arial;background:#eef2f7;margin:30px}
main{max-width:500px;margin:auto;background:white;padding:25px;border-radius:12px}
input,button{padding:12px;margin:7px}
button{cursor:pointer}
</style></head><body><main>
<h1>BMI Calculator</h1>
<label>Weight (kg)<br><input id="weight" type="number" min="1" step="any"></label><br>
<label>Height (cm)<br><input id="height" type="number" min="1" step="any"></label><br>
<button onclick="calculate()">Calculate BMI</button>
<h2 id="result"></h2><p id="category"></p>
<script>
async function calculate(){
 const w=Number(weight.value),h=Number(height.value);
 if(!weight.value||!height.value||w<=0||h<=0){
   result.textContent='Enter valid positive measurements';category.textContent='';return;
 }
 const r=await fetch('/api/bmi',{
   method:'POST',headers:{'Content-Type':'application/json'},
   body:JSON.stringify({weight:w,height:h})
 });
 const data=await r.json();
 if(!r.ok){result.textContent=data.error;return;}
 result.textContent='BMI: '+data.bmi;
 category.textContent='Category: '+data.category;
}
</script></main></body></html>
"""

@app.get("/")
def home():
    return render_template_string(PAGE)

@app.get("/api/health")
def health():
    return jsonify(status="ok", app="bmi-calculator")

@app.post("/api/bmi")
def calculate_bmi():
    data = request.get_json(silent=True) or {}
    try:
        weight = float(data["weight"])
        height = float(data["height"]) / 100
    except (KeyError, TypeError, ValueError):
        return jsonify(error="Enter valid measurements"), 400

    import math
    if (not math.isfinite(weight) or not math.isfinite(height)
            or weight <= 0 or height <= 0):
        return jsonify(error="Measurements must be positive"), 400

    bmi = weight / (height * height)
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal range"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obesity range"

    return jsonify(bmi=round(bmi, 2), category=category)

if __name__ == "__main__":
    app.run(host="0.0.0.0",
            port=int(os.environ.get("PORT", "5000")))
