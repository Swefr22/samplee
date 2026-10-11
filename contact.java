
import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpExchange;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.io.OutputStream;

public class Main {
    static final String PAGE = """
    <!DOCTYPE html><html><head>
    <title>Contact Book</title>
    <meta name="viewport" content="width=device-width">
    <style>
    body{font:17px Arial;background:#eef2f7;margin:30px}
    main{max-width:650px;margin:auto;background:white;padding:25px;border-radius:12px}
    input,button{padding:10px;margin:5px}
    li{margin:12px 0}
    </style></head><body><main>
    <h1>Contact Book</h1>
    <input id="name" placeholder="Name">
    <input id="phone" placeholder="Phone number">
    <button onclick="add()">Add Contact</button>
    <p><input id="search" placeholder="Search contacts" oninput="draw()"></p>
    <ul id="list"></ul>
    <script>
    let contacts=[];
    function draw(){
      list.innerHTML='';
      const q=search.value.toLowerCase();
      contacts.filter(c=>(c.name+' '+c.phone).toLowerCase().includes(q))
      .forEach(c=>{
        let li=document.createElement('li');
        li.textContent=c.name+' — '+c.phone+' ';
        let b=document.createElement('button');
        b.textContent='Delete';
        b.onclick=()=>{contacts=contacts.filter(x=>x.id!==c.id);draw();};
        li.appendChild(b);list.appendChild(li);
      });
    }
    function add(){
      const n=name.value.trim(),p=phone.value.trim();
      if(!n||!p){alert('Enter both name and phone');return;}
      contacts.push({id:Date.now()+Math.random(),name:n,phone:p});
      name.value='';phone.value='';draw();
    }
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
                 "{\"status\":\"ok\",\"app\":\"contact-book\"}"));
        server.createContext("/",ex->send(ex,200,"text/html",PAGE));
        server.start();
        System.out.println("Contact Book running on port "+port);
    }
}
