
import com.sun.net.httpserver.HttpServer;
import java.net.InetSocketAddress;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.io.OutputStream;
import java.time.LocalDate;
import java.time.Period;

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

        server.createContext("/api/age", ex -> {
            String query = ex.getRequestURI().getRawQuery();
            String dob = "";
            if (query != null) {
                for (String part : query.split("&")) {
                    String[] pair = part.split("=", 2);
                    if (pair.length == 2 && pair[0].equals("dob")) {
                        dob = URLDecoder.decode(pair[1], StandardCharsets.UTF_8);
                    }
                }
            }
            try {
                LocalDate birthDate = LocalDate.parse(dob);
                LocalDate today = LocalDate.now();
                if (birthDate.isAfter(today)) {
                    send(ex, 400, "application/json",
                         "{\"error\":\"Date of birth cannot be in the future.\"}");
                    return;
                }
                int age = Period.between(birthDate, today).getYears();
                send(ex, 200, "application/json",
                     "{\"age\":" + age + ",\"dob\":\"" + dob + "\"}");
            } catch (Exception e) {
                send(ex, 400, "application/json",
                     "{\"error\":\"Enter a valid date of birth.\"}");
            }
        });

        server.createContext("/", ex -> {
            String html = """
            <!DOCTYPE html><html><head><meta charset="UTF-8"><title>Age Calculator</title>
            <style>
            body{font-family:Arial;background:#f2f5ff;display:grid;place-items:center;min-height:90vh}
            main{background:white;padding:30px;border-radius:16px;width:min(380px,85vw);box-shadow:0 4px 16px #ccd}
            input,button{box-sizing:border-box;width:100%;padding:12px;margin:10px 0;border-radius:8px}
            input{border:1px solid #aaa}button{background:#3549a6;color:white;border:0;cursor:pointer}
            #result{font-size:20px;font-weight:bold;color:#3549a6}
            </style></head><body><main><h1>Age Calculator</h1>
            <label>Select your date of birth</label>
            <input type="date" id="dob">
            <button onclick="calculateAge()">Calculate Age</button><p id="result"></p>
            <script>
            async function calculateAge(){
              const dob=document.getElementById('dob').value;
              const out=document.getElementById('result');
              if(!dob){out.textContent='Please select your birth date.';return;}
              const response=await fetch('/api/age?dob='+encodeURIComponent(dob));
              const data=await response.json();
              out.textContent=response.ok?'Your age is '+data.age+' years.':data.error;
            }
            </script></main></body></html>
            """;
            send(ex, 200, "text/html", html);
        });

        server.start();
        System.out.println("Age Calculator running at http://localhost:" + port);
    }
}
