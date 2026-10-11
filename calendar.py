
from flask import Flask, request, jsonify, render_template_string
from datetime import date
import os

app = Flask(__name__)

PAGE = """
<!DOCTYPE html><html><head><title>Calendar Picker</title>
<style>
body{font-family:Arial;background:#f0faf7;display:grid;place-items:center;min-height:90vh}
main{background:white;padding:30px;border-radius:16px;width:min(380px,85vw);box-shadow:0 4px 15px #ccd}
input,button{box-sizing:border-box;width:100%;padding:12px;margin:10px 0;border-radius:8px}
input{border:1px solid #aaa}button{background:#087f65;color:white;border:0;cursor:pointer}
#result{color:#087f65;font-weight:bold}
</style></head><body><main><h1>Calendar Picker</h1>
<p>Select a date using the calendar.</p>
<input type="date" id="pickedDate">
<button onclick="submitDate()">Confirm Date</button><p id="result"></p>
<script>
async function submitDate(){
 const selected=document.getElementById('pickedDate').value;
 const out=document.getElementById('result');
 if(!selected){out.textContent='Please select a date.';return;}
 const r=await fetch('/api/date',{
   method:'POST',headers:{'Content-Type':'application/json'},
   body:JSON.stringify({date:selected})
 });
 const d=await r.json();
 out.textContent=r.ok?'Selected: '+d.formatted:'Error: '+d.error;
}
</script></main></body></html>
"""

@app.get("/")
def home():
    return render_template_string(PAGE)

@app.get("/api/health")
def health():
    return jsonify(status="ok")

@app.post("/api/date")
def choose_date():
    data = request.get_json(silent=True) or {}
    try:
        selected = date.fromisoformat(str(data.get("date", "")))
        return jsonify(
            date=selected.isoformat(),
            formatted=selected.strftime("%d %B %Y")
        )
    except ValueError:
        return jsonify(error="Enter a valid date in YYYY-MM-DD format."), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
