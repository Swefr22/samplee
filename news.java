
import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpExchange;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.io.OutputStream;

public class Main {
    static final String PAGE = """
    <!DOCTYPE html><html><head><title>News Feed</title>
    <meta name="viewport" content="width=device-width">
    <style>
    body{font:17px Arial;background:#eef2f7;margin:30px}
    main{max-width:700px;margin:auto;background:white;padding:25px;border-radius:12px}
    input{padding:12px;width:80%}
    article{padding:15px;margin:12px 0;background:#f1f5f9;border-radius:8px}
    </style></head><body><main>
    <h1>Campus News Feed</h1>
    <input id="search" placeholder="Search headlines" oninput="draw()">
    <div id="articles"></div>
    <script>
    const news=[
      {title:'Students Showcase New AI Projects',category:'Technology',
       detail:'Student teams present practical AI prototypes.'},
      {title:'College Hosts Innovation Workshop',category:'Education',
       detail:'A workshop introduces design thinking and prototyping.'},
      {title:'Open-Source Tools Support Faster Deployments',category:'Software',
       detail:'Automation helps teams build and test applications.'},
      {title:'Research Teams Explore Clean Energy',category:'Science',
       detail:'Student researchers discuss sustainable technology.'}
    ];
    function draw(){
      articles.innerHTML='';
      news.filter(n=>(n.title+' '+n.category+' '+n.detail)
        .toLowerCase().includes(search.value.toLowerCase()))
      .forEach(n=>{
        let card=document.createElement('article');
        let h=document.createElement('h3');h.textContent=n.title;
        let c=document.createElement('b');c.textContent=n.category;
        let p=document.createElement('p');p.textContent=n.detail;
        card.append(h,c,p);articles.appendChild(card);
      });
      if(!articles.children.length)articles.textContent='No articles found.';
    }
    draw();
    </script></main></body></html>
    """;

    static void send(HttpExchange ex,int code,String type,String body)
            throws java.io.IOException {
        byte[] bytes=body.getBytes(StandardCharsets.UTF_8);
        ex.getResponseHeaders().set("Content-Type",type+"; charset=UTF-8");
        ex.sendResponseHeaders(code,bytes.length);
        try(OutputStream out=ex.getResponseBody()){out.write(bytes);}
    }

    public static void main(String[] args)throws Exception {
        int port=Integer.parseInt(System.getenv().getOrDefault("PORT","8080"));
        HttpServer server=HttpServer.create(new InetSocketAddress(port),0);
        server.createContext("/api/health",ex->
            send(ex,200,"application/json",
                 "{\"status\":\"ok\",\"app\":\"news\"}"));
        server.createContext("/",ex->send(ex,200,"text/html",PAGE));
        server.start();
        System.out.println("News app running on port "+port);
    }
}
