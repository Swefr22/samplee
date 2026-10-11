
from flask import Flask, jsonify, render_template_string
import os
from threading import Lock

app = Flask(__name__)
count = 0
lock = Lock()

PAGE = """
<!DOCTYPE html><html><head><title>Counter App</title>
<style>
body{font-family:Arial;background:#edf6ff;display:grid;place-items:center;min-height:90vh}
main{background:white;padding:35px;border-radius:18px;text-align:center;width:300px;box-shadow:0 4px 15px #ccd}
#count{font-size:60px;color:#1769aa;margin:25px}
button{padding:12px 18px;margin:5px;border:0;border-radius:8px;background:#1769aa;color:white;cursor:pointer}
.reset{background:#666}
</style></head><body><main><h1>Counter App</h1>
<div id="count">0</div>
<button onclick="change('/api/increment')">+ Increment</button>
<button onclick="change('/api/decrement')">− Decrement</button>
<button class="reset" onclick="change('/api/reset')">Reset</button>
<script>
async function refresh(){
 const r=await fetch('/api/count');
 const d=await r.json();
 document.getElementById('count').textContent=d.count;
}
async function change(path){
 await fetch(path,{method:'POST'});
 await refresh();
}
refresh();
</script></main></body></html>
"""

@app.get("/")
def home():
    return render_template_string(PAGE)

@app.get("/api/health")
def health():
    return jsonify(status="ok")

@app.get("/api/count")
def get_count():
    with lock:
        return jsonify(count=count)

@app.post("/api/increment")
def increment():
    global count
    with lock:
        count += 1
        return jsonify(count=count)

@app.post("/api/decrement")
def decrement():
    global count
    with lock:
        count -= 1
        return jsonify(count=count)

@app.post("/api/reset")
def reset():
    global count
    with lock:
        count = 0
        return jsonify(count=count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
