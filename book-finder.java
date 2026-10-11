
import com.sun.net.httpserver.HttpServer;
import java.net.InetSocketAddress;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.io.OutputStream;
import java.util.List;

public class Main {
    record Book(String title, String author, String category) {}

    static final List<Book> BOOKS = List.of(
        new Book("Wings of Fire", "A. P. J. Abdul Kalam", "Autobiography"),
        new Book("The Alchemist", "Paulo Coelho", "Fiction"),
        new Book("Atomic Habits", "James Clear", "Self-help"),
        new Book("Clean Code", "Robert C. Martin", "Programming"),
        new Book("Deep Learning", "Ian Goodfellow", "Technology")
    );

    static void send(com.sun.net.httpserver.HttpExchange ex, int status,
                     String type, String body) throws java.io.IOException {
        byte[] data = body.getBytes(StandardCharsets.UTF_8);
        ex.getResponseHeaders().set("Content-Type", type + "; charset=UTF-8");
        ex.sendResponseHeaders(status, data.length);
        try (OutputStream os = ex.getResponseBody()) { os.write(data); }
    }

    static String escape(String s) {
        return s.replace("&", "&amp;").replace("\"", "&quot;")
                .replace("<", "&lt;").replace(">", "&gt;");
    }

    public static void main(String[] args) throws Exception {
        int port = Integer.parseInt(System.getenv().getOrDefault("PORT", "8080"));
        HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);

        server.createContext("/api/health", ex ->
            send(ex, 200, "application/json", "{\"status\":\"ok\"}"));

        server.createContext("/api/books", ex -> {
            String query = "";
            if (ex.getRequestURI().getRawQuery() != null) {
                for (String part : ex.getRequestURI().getRawQuery().split("&")) {
                    String[] pair = part.split("=", 2);
                    if (pair.length == 2 && pair[0].equals("q")) {
                        query = URLDecoder.decode(pair[1], StandardCharsets.UTF_8);
                    }
                }
            }
            String q = query.toLowerCase();
            StringBuilder json = new StringBuilder("[");
            boolean first = true;
            for (Book b : BOOKS) {
                if (b.title().toLowerCase().contains(q)
                        || b.author().toLowerCase().contains(q)) {
                    if (!first) json.append(",");
                    json.append("{\"title\":\"").append(escape(b.title()))
                        .append("\",\"author\":\"").append(escape(b.author()))
                        .append("\",\"category\":\"").append(escape(b.category()))
                        .append("\"}");
                    first = false;
                }
            }
            json.append("]");
            send(ex, 200, "application/json", json.toString());
        });

        server.createContext("/", ex -> {
            String html = """
            <!DOCTYPE html><html><head><meta charset="UTF-8"><title>Book Finder</title>
            <style>
            body{font-family:Arial;background:#f4f0ff;padding:30px}
            main{max-width:750px;margin:auto}input,button{padding:12px;border-radius:8px}
            input{width:65%;border:1px solid #aaa}button{background:#5b21b6;color:white;border:0}
            .book{background:white;padding:15px;margin:12px 0;border-radius:10px}
            </style></head><body><main><h1>Book Finder</h1>
            <p>Search by book title or author.</p>
            <input id="query" placeholder="Try Clean Code or James Clear">
            <button onclick="searchBooks()">Search</button><div id="results"></div>
            <script>
            async function searchBooks(){
              const q=document.getElementById('query').value;
              const response=await fetch('/api/books?q='+encodeURIComponent(q));
              const books=await response.json();
              const out=document.getElementById('results');out.replaceChildren();
              if(!books.length){out.textContent='No books found.';return;}
              books.forEach(b=>{
                const card=document.createElement('div');card.className='book';
                const title=document.createElement('h2');title.textContent=b.title;card.appendChild(title);
                const author=document.createElement('p');author.textContent='Author: '+b.author;card.appendChild(author);
                const category=document.createElement('p');category.textContent='Category: '+b.category;card.appendChild(category);
                out.appendChild(card);
              });
            }
            searchBooks();
            </script></main></body></html>
            """;
            send(ex, 200, "text/html", html);
        });

        server.start();
        System.out.println("Book Finder running at http://localhost:" + port);
    }
}
