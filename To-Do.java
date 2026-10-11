
import com.sun.net.httpserver.HttpServer;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.io.OutputStream;

public class Main {
    static final String PAGE = """
    <!DOCTYPE html>
    <html>
    <head>
      <title>To-Do List</title>
      <meta name="viewport" content="width=device-width">
      <style>
        body{font:18px Arial;max-width:650px;margin:40px auto;padding:15px;background:#eef2f7}
        main{background:white;padding:25px;border-radius:12px}
        input,button{padding:10px;margin:5px}
        button{cursor:pointer} li{margin:12px}
      </style>
    </head>
    <body><main>
      <h1>My To-Do List</h1>
      <input id="task" placeholder="Enter a task">
      <button onclick="add()">Add Task</button>
      <ul id="items"></ul>
      <p id="status"></p>
    </main>
    <script>
      let tasks=[];
      function draw(){
        items.innerHTML='';
        tasks.forEach((t,i)=>{
          let li=document.createElement('li');
          let label=document.createElement('span');
          label.textContent=t;
          let edit=document.createElement('button');
          edit.textContent='Edit';
          edit.onclick=()=>{
            let v=prompt('Edit task',tasks[i]);
            if(v && v.trim()){tasks[i]=v.trim();draw();}
          };
          let del=document.createElement('button');
          del.textContent='Delete';
          del.onclick=()=>{tasks.splice(i,1);draw();};
          li.append(label,edit,del);
          items.appendChild(li);
        });
        status.textContent=tasks.length+' task(s)';
      }
      function add(){
        if(task.value.trim()){
          tasks.push(task.value.trim());
          task.value='';
          draw();
        }
      }
      task.addEventListener('keydown',e=>{if(e.key==='Enter')add()});
    </script>
    </body></html>
    """;

    static void send(com.sun.net.httpserver.HttpExchange ex,
                     int code, String type, String body)
                     throws java.io.IOException {
        byte[] data=body.getBytes(StandardCharsets.UTF_8);
        ex.getResponseHeaders().set("Content-Type",type+"; charset=UTF-8");
        ex.sendResponseHeaders(code,data.length);
        try(OutputStream os=ex.getResponseBody()){os.write(data);}
    }

    public static void main(String[] args) throws Exception {
        int port=Integer.parseInt(
            System.getenv().getOrDefault("PORT","8080"));
        HttpServer server=HttpServer.create(
            new InetSocketAddress(port),0);

        server.createContext("/api/health",ex->
            send(ex,200,"application/json",
                 "{\"status\":\"ok\",\"app\":\"todo\"}"));

        server.createContext("/",ex->
            send(ex,200,"text/html",PAGE));

        server.start();
        System.out.println("To-Do app running on port "+port);
    }
}
