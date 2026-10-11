
from flask import Flask, request, jsonify, render_template_string
import os
import math

app = Flask(__name__)

PAGE = """
<!DOCTYPE html><html><head><title>Shopping Bill Calculator</title>
<style>
body{font-family:Arial;background:#f4f7ed;display:grid;place-items:center;min-height:90vh}
main{background:white;padding:28px;border-radius:16px;width:min(420px,88vw);box-shadow:0 4px 15px #ccd}
input,button{box-sizing:border-box;width:100%;padding:12px;margin:8px 0;border-radius:8px}
input{border:1px solid #bbb}button{background:#47732c;color:white;border:0;cursor:pointer}
#result{white-space:pre-line;font-size:17px;line-height:1.8}
</style></head><body><main><h1>Shopping Bill</h1>
<label>Item name</label><input id="name" placeholder="Notebook">
<label>Price per item (₹)</label><input id="price" type="number" min="0" step="any" value="50">
<label>Quantity</label><input id="quantity" type="number" min="1" step="1" value="2">
<label>Tax (%)</label><input id="tax" type="number" min="0" max="100" step="any" value="5">
<button onclick="calculate()">Calculate Bill</button><p id="result"></p>
<script>
async function calculate(){
 const data={
   name:document.getElementById('name').value,
   price:document.getElementById('price').value,
   quantity:document.getElementById('quantity').value,
   tax:document.getElementById('tax').value
 };
 const r=await fetch('/api/bill',{
   method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)
 });
 const d=await r.json();
 document.getElementById('result').textContent=r.ok?
   'Item: '+d.name+'\\nSubtotal: ₹'+d.subtotal.toFixed(2)+
   '\\nTax: ₹'+d.taxAmount.toFixed(2)+'\\nTotal: ₹'+d.total.toFixed(2):
   d.error;
}
</script></main></body></html>
"""

@app.get("/")
def home():
    return render_template_string(PAGE)

@app.get("/api/health")
def health():
    return jsonify(status="ok")

@app.post("/api/bill")
def calculate_bill():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()

    try:
        price = float(data.get("price", ""))
        quantity = int(data.get("quantity", ""))
        tax_rate = float(data.get("tax", ""))

        if not name:
            raise ValueError("Enter an item name.")
        if not math.isfinite(price) or price < 0:
            raise ValueError("Price must be a non-negative number.")
        if quantity < 1 or quantity > 100000:
            raise ValueError("Quantity must be between 1 and 100000.")
        if not math.isfinite(tax_rate) or not 0 <= tax_rate <= 100:
            raise ValueError("Tax must be between 0 and 100 percent.")

    except (ValueError, TypeError) as e:
        message = str(e) or "Enter valid price, quantity, and tax values."
        return jsonify(error=message), 400

    subtotal = price * quantity
    tax_amount = subtotal * tax_rate / 100
    total = subtotal + tax_amount

    return jsonify(
        name=name,
        subtotal=round(subtotal, 2),
        taxAmount=round(tax_amount, 2),
        total=round(total, 2)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
