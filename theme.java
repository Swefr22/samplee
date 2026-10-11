
import com.sun.net.httpserver.HttpServer;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.io.OutputStream;

public class Main {
    static void send(com.sun.net.httpserver.HttpExchange ex, int code,
                     String type, String body) throws java.io.IOException {
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

        server.createContext("/", ex -> {
            String html = """
            <!DOCTYPE html><html><head><meta charset="UTF-8"><title>Theme Switcher</title>
            <style>
            :root{--bg:#f3f7fb;--fg:#172033;--card:#fff;--accent:#087f8c}
            body.dark{--bg:#151a23;--fg:#edf2f7;--card:#242c39;--accent:#43c6c9}
            body{font-family:Arial;background:var(--bg);color:var(--fg);min-height:90vh;
              display:grid;place-items:center;transition:background .2s,color .2s}
            main{background:var(--card);padding:35px;border-radius:18px;
              max-width:460px;margin:20px;box-shadow:0 5px 20px #8884}
            button{background:var(--accent);color:white;border:0;border-radius:9px;
              padding:12px 18px;cursor:pointer;font-size:16px}
            </style></head><body><main>
            <h1>Theme Switcher</h1>
            <p>Change the appearance of this page with one click.</p>
            <button id="toggle">Switch Theme</button>
            <p id="status"></p>
            </main>
            <script>
            const body=document.body;
            const status=document.getElementById('status');
            const toggle=document.getElementById('toggle');
            function applyTheme(theme){
              body.classList.toggle('dark',theme==='dark');
              status.textContent='Current theme: '+theme;
              toggle.textContent=theme==='dark'?'Switch to Light':'Switch to Dark';
            }
            let saved='light';
            try{saved=localStorage.getItem('theme')||'light';}catch(e){}
            applyTheme(saved);
            toggle.addEventListener('click',()=>{
              const theme=body.classList.contains('dark')?'light':'dark';
              applyTheme(theme);
              try{localStorage.setItem('theme',theme);}catch(e){}
            });
            </script></body></html>
            """;
            send(ex, 200, "text/html", html);
        });

        server.start();
        System.out.println("Theme Switcher running at http://localhost:" + port);
    }
}
