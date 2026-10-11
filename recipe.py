
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

RECIPES = [
    {
        "name": "Tomato Pasta",
        "ingredients": ["pasta", "tomato", "garlic", "oil", "salt"],
        "instructions": "Boil pasta. Saute garlic and tomato in oil. Mix with pasta and salt."
    },
    {
        "name": "Vegetable Fried Rice",
        "ingredients": ["rice", "carrot", "beans", "onion", "soy sauce"],
        "instructions": "Cook rice. Saute chopped vegetables, add rice and soy sauce, then mix."
    },
    {
        "name": "Banana Pancakes",
        "ingredients": ["banana", "flour", "milk", "sugar"],
        "instructions": "Mash banana. Mix with flour, milk and sugar. Cook small portions on a pan."
    },
    {
        "name": "Omelette",
        "ingredients": ["egg", "onion", "salt", "pepper"],
        "instructions": "Beat eggs with chopped onion and seasoning. Cook in a lightly oiled pan."
    }
]

PAGE = """
<!DOCTYPE html><html><head><title>Recipe Finder</title>
<style>
body{font-family:Arial;background:#fff8ef;margin:0;padding:30px}
main{max-width:800px;margin:auto}input,button{padding:12px;border-radius:8px}
input{width:65%;border:1px solid #bbb}button{background:#b45309;color:white;border:0}
.card{background:white;padding:18px;margin:15px 0;border-radius:12px;box-shadow:0 2px 8px #ddd}
h1{color:#92400e}
</style></head><body><main><h1>Recipe Finder</h1>
<p>Search by recipe name or ingredient.</p>
<input id="query" placeholder="Try tomato, rice, or banana">
<button onclick="searchRecipes()">Search</button><div id="results"></div>
<script>
async function searchRecipes(){
 const q=document.getElementById('query').value;
 const response=await fetch('/api/recipes?q='+encodeURIComponent(q));
 const recipes=await response.json();
 const out=document.getElementById('results'); out.replaceChildren();
 if(!recipes.length){out.textContent='No recipes found.';return;}
 recipes.forEach(r=>{
   const card=document.createElement('section');card.className='card';
   const title=document.createElement('h2');title.textContent=r.name;card.appendChild(title);
   const ing=document.createElement('p');ing.textContent='Ingredients: '+r.ingredients.join(', ');card.appendChild(ing);
   const ins=document.createElement('p');ins.textContent='Instructions: '+r.instructions;card.appendChild(ins);
   out.appendChild(card);
 });
}
searchRecipes();
</script></main></body></html>
"""

@app.get("/")
def home():
    return render_template_string(PAGE)

@app.get("/api/health")
def health():
    return jsonify(status="ok")

@app.get("/api/recipes")
def recipes():
    query = request.args.get("q", "").strip().lower()
    results = [
        recipe for recipe in RECIPES
        if query in recipe["name"].lower()
        or any(query in item.lower() for item in recipe["ingredients"])
    ]
    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(__import__("os").environ.get("PORT", 5000)))
