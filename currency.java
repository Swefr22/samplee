
import com.sun.net.httpserver.HttpServer;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.io.OutputStream;

public class Main {
    static void send(com.sun.net.httpserver.HttpExchange ex, int code, String type, String body)
            throws java.io.IOException {
        byte[] data = body.getBytes(StandardCharsets.UTF_8);
        ex.getResponseHeaders().set("Content-Type", type + "; charset=UTF-8");
        ex.sendResponseHeaders(code, data.length);
        try (OutputStream os = ex.getResponseBody()) { os.write(data); }
    }

    public static void main(String[] args) throws Exception {
        int port = Integer.parseInt(System.getenv().getOrDefault("PORT", "8080"));
        HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);

        server.createContext("/api/health", ex ->
            send(ex, 200, "application/json", "{\"status\":\"ok\"}"));

        server.createContext("/api/convert", ex -> {
            if (!ex.getRequestMethod().equals("GET")) {
                send(ex, 405, "application/json", "{\"error\":\"Use GET\"}");
                return;
            }
            String query = ex.getRequestURI().getQuery();
            java.util.Map<String, String> p = new java.util.HashMap<>();
            if (query != null) for (String part : query.split("&")) {
                String[] pair = part.split("=", 2);
                if (pair.length == 2) p.put(pair[0], java.net.URLDecoder.decode(pair[1], "UTF-8"));
            }
            try {
                double amount = Double.parseDouble(p.getOrDefault("amount", "1"));
                String from = p.getOrDefault("from", "USD");
                String to = p.getOrDefault("to", "INR");
                java.util.Map<String, Double> rates = java.util.Map.of(
                    "USD", 1.0, "INR", 83.0, "EUR", 0.92, "GBP", 0.79
                );
                if (amount < 0 || !Double.isFinite(amount)
                        || !rates.containsKey(from) || !rates.containsKey(to)) {
                    send(ex, 400, "application/json", "{\"error\":\"Invalid amount or currency\"}");
                    return;
                }
                double result = amount / rates.get(from) * rates.get(to);
                send(ex, 200, "application/json",
                    String.format(java.util.Locale.US,
                        "{\"amount\":%.2f,\"from\":\"%s\",\"to\":\"%s\",\"result\":%.2f}",
                        amount, from, to, result));
            } catch (Exception e) {
                send(ex, 400, "application/json", "{\"error\":\"Enter a valid amount\"}");
            }
        });

        server.createContext("/", ex -> {
            String html = """
            <!DOCTYPE html><html><head><meta charset="UTF-8"><title>Currency Converter</title>
            <style>
            body{font-family:Arial;background:#eef5f5;display:grid;place-items:center;min-height:90vh}
            main{background:white;padding:28px;border-radius:16px;width:min(380px,85vw);box-shadow:0 5px 20px #ccd}
            input,select,button{box-sizing:border-box;width:100%;padding:12px;margin:8px 0;border:1px solid #bbb;border-radius:8px}
            button{background:#087f8c;color:white;border:0;cursor:pointer}
            #result{font-size:20px;font-weight:bold;color:#087f8c}
            </style></head><body><main><h1>Currency Converter</h1>
            <p>Sample rates: 1 USD = ₹83, €0.92, £0.79</p>
            <input id="amount" type="number" min="0" step="any" value="1">
            <select id="from"><option>USD</option><option>INR</option><option>EUR</option><option>GBP</option></select>
            <label>Convert to</label>
            <select id="to"><option>INR</option><option>USD</option><option>EUR</option><option>GBP</option></select>
            <button onclick="convert()">Convert</button><p id="result"></p>
            <script>
            async function convert(){
              const q=new URLSearchParams({amount:amount.value,from:from.value,to:to.value});
              const r=await fetch('/api/convert?'+q);
              const d=await r.json();
              document.getElementById('result').textContent=r.ok?
                d.amount+' '+d.from+' = '+d.result+' '+d.to:d.error;
            }
            </script></main></body></html>
            """;
            send(ex, 200, "text/html", html);
        });

        server.start();
        System.out.println("Currency Converter running at http://localhost:" + port);
    }
}
