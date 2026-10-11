
import com.sun.net.httpserver.HttpServer;
import java.net.InetSocketAddress;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.io.OutputStream;

public class Main {
    static void send(com.sun.net.httpserver.HttpExchange ex, int status,
                     String type, String body) throws java.io.IOException {
        byte[] data = body.getBytes(StandardCharsets.UTF_8);
        ex.getResponseHeaders().set("Content-Type", type + "; charset=UTF-8");
        ex.sendResponseHeaders(status, data.length);
        try (OutputStream os = ex.getResponseBody()) { os.write(data); }
    }

    public static void main(String[] args) throws Exception {
        int port = Integer.parseInt(System.getenv().getOrDefault("PORT", "8080"));
        HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);

        server.createContext("/api/health", ex ->
            send(ex, 200, "application/json", "{\"status\":\"ok\"}"));

        server.createContext("/api/discount", ex -> {
            String query = ex.getRequestURI().getRawQuery();
            java.util.Map<String, String> params = new java.util.HashMap<>();
            if (query != null) {
                for (String part : query.split("&")) {
                    String[] pair = part.split("=", 2);
                    if (pair.length == 2) {
                        params.put(pair[0],
                            URLDecoder.decode(pair[1], StandardCharsets.UTF_8));
                    }
                }
            }
            try {
                double price = Double.parseDouble(params.getOrDefault("price", ""));
                double percent = Double.parseDouble(params.getOrDefault("percent", ""));
                if (!Double.isFinite(price) || !Double.isFinite(percent)
                        || price < 0 || percent < 0 || percent > 100) {
                    send(ex, 400, "application/json",
                         "{\"error\":\"Price must be non-negative and discount 0-100%.\"}");
                    return;
                }
                double discount = price * percent / 100.0;
                double finalPrice = price - discount;
                send(ex, 200, "application/json",
                    String.format(java.util.Locale.US,
                        "{\"discount\":%.2f,\"finalPrice\":%.2f}",
                        discount, finalPrice));
            } catch (Exception e) {
                send(ex, 400, "application/json",
                     "{\"error\":\"Enter valid numeric values.\"}");
            }
        });

        server.createContext("/", ex -> {
            String html = """
            <!DOCTYPE html><html><head><meta charset="UTF-8"><title>Discount Calculator</title>
            <style>
            body{font-family:Arial;background:#fff7ed;display:grid;place-items:center;min-height:90vh}
            main{background:white;padding:30px;border-radius:16px;width:min(380px,85vw);box-shadow:0 4px 15px #ddd}
            input,button{box-sizing:border-box;width:100%;padding:12px;margin:10px 0;border-radius:8px}
            input{border:1px solid #bbb}button{background:#c2410c;color:white;border:0;cursor:pointer}
            #result{font-size:18px;line-height:1.7}
            </style></head><body><main><h1>Discount Calculator</h1>
            <label>Original price (₹)</label><input id="price" type="number" min="0" step="any" value="1000">
            <label>Discount (%)</label><input id="percent" type="number" min="0" max="100" value="10">
            <button onclick="calculate()">Calculate</button><div id="result"></div>
            <script>
            async function calculate(){
              const p=document.getElementById('price').value;
              const d=document.getElementById('percent').value;
              const out=document.getElementById('result');
              const q=new URLSearchParams({price:p,percent:d});
              const r=await fetch('/api/discount?'+q);
              const data=await r.json();
              out.textContent=r.ok?
                'Discount: ₹'+data.discount.toFixed(2)+' | Final price: ₹'+data.finalPrice.toFixed(2):
                data.error;
            }
            </script></main></body></html>
            """;
            send(ex, 200, "text/html", html);
        });

        server.start();
        System.out.println("Discount Calculator running at http://localhost:" + port);
    }
}
