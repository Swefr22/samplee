
from flask import Flask, jsonify, request, render_template_string
import os

app = Flask(__name__)

WORDS = {
    "algorithm": "A sequence of steps used to solve a problem.",
    "deploy": "To release software so it can be used.",
    "pipeline": "An automated sequence of build, test, and delivery steps.",
    "resilient": "Able to recover quickly from difficulty.",
    "debug": "To identify and fix errors in a program.",
    "repository": "A place where project files and their history are stored.",
    "automation": "Using technology to perform tasks with less manual effort."
}

PAGE = """
<!DOCTYPE html><html><head><title>Dictionary</title>
<meta name="viewport" content="width=device-width">
<style>
body{font:18px Arial;background:#eef2f7;margin:30px}
main{max-width:600px;margin:auto;background:white;padding:25px;border-radius:12px}
input,button{padding:12px;margin:5px}
button{cursor:pointer}
</style></head><body><main>
<h1>Mini Dictionary</h1>
<input id="word" placeholder="Enter a word">
<button onclick="searchWord()">Search</button>
<h2 id="term"></h2><p id="meaning"></p>
<script>
async function searchWord(){
 const w=word.value.trim();
 if(!w){term.textContent='';meaning.textContent='Enter a word';return;}
 const r=await fetch('/api/meaning?word='+encodeURIComponent(w));
 const data=await r.json();
 term.textContent=data.word||'';
 meaning.textContent=data.meaning||data.error;
}
word.addEventListener('keydown',e=>{if(e.key==='Enter')searchWord()});
</script></main></body></html>
"""

@app.get("/")
def home():
    return render_template_string(PAGE)

@app.get("/api/health")
def health():
    return jsonify(status="ok", app="dictionary")

@app.get("/api/meaning")
def meaning():
    word = request.args.get("word", "").strip().lower()
    if not word:
        return jsonify(error="Enter a word"), 400
    definition = WORDS.get(word)
    if definition is None:
        return jsonify(word=word, error="Word not found in this demo dictionary")
    return jsonify(word=word, meaning=definition)

if __name__ == "__main__":
    app.run(host="0.0.0.0",
            port=int(os.environ.get("PORT", "5000")))
