
from flask import Flask, jsonify, request, render_template_string
import os

app = Flask(__name__)
expenses = []
next_id = 1

PAGE = """
<!DOCTYPE html>
<html><head><title>Expense Tracker</title>
<meta name="viewport" content="width=device-width">
<style>
body{font:17px Arial;background:#eef2f7;margin:30px}
main{max-width:650px;margin:auto;background:white;padding:25px;border-radius:12px}
input,button{padding:10px;margin:5px}
button{cursor:pointer}
li{margin:12px 0}
</style></head><body><main>
<h1>Expense Tracker</h1>
<input id="name" placeholder="Expense name">
<input id="amount" type="number" min="0.01" step="0.01" placeholder="Amount">
<button onclick="addExpense()">Add Expense</button>
<h2 id="total">Total: ₹0.00</h2>
<ul id="list"></ul>
<script>
async function load(){
 const r=await fetch('/api/expenses');
 const data=await r.json();
 list.innerHTML='';
 let total=0;
 data.forEach(e=>{
   total+=e.amount;
   const li=document.createElement('li');
   li.textContent=e.name+' — ₹'+e.amount.toFixed(2)+' ';
   const b=document.createElement('button');
   b.textContent='Delete';
   b.onclick=()=>removeExpense(e.id);
   li.appendChild(b);list.appendChild(li);
 });
 document.getElementById('total').textContent=
   'Total: ₹'+total.toFixed(2);
}
async function addExpense(){
 const n=name.value.trim(),a=Number(amount.value);
 if(!n||amount.value===''||!Number.isFinite(a)||a<=0){
   alert('Enter a name and a positive amount');return;
 }
 const r=await fetch('/api/expenses',{
   method:'POST',headers:{'Content-Type':'application/json'},
   body:JSON.stringify({name:n,amount:a})
 });
 if(r.ok){name.value='';amount.value='';load();}
 else alert('Could not add expense');
}
async function removeExpense(id){
 await fetch('/api/expenses/'+id,{method:'DELETE'});load();
}
load();
</script></main></body></html>
"""

@app.get("/")
def home():
    return render_template_string(PAGE)

@app.get("/api/health")
def health():
    return jsonify(status="ok", app="expense-tracker")

@app.get("/api/expenses")
def get_expenses():
    return jsonify(expenses)

@app.post("/api/expenses")
def add_expense():
    global next_id
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    try:
        amount = float(data.get("amount"))
    except (TypeError, ValueError):
        return jsonify(error="Invalid amount"), 400
    if not name or not __import__("math").isfinite(amount) or amount <= 0:
        return jsonify(error="Name and positive amount required"), 400
    item = {"id": next_id, "name": name, "amount": amount}
    next_id += 1
    expenses.append(item)
    return jsonify(item), 201

@app.delete("/api/expenses/<int:item_id>")
def delete_expense(item_id):
    for item in expenses:
        if item["id"] == item_id:
            expenses.remove(item)
            return jsonify(deleted=True)
    return jsonify(error="Not found"), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0",
            port=int(os.environ.get("PORT", "5000")))
