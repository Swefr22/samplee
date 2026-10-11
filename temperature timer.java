
import com.sun.net.httpserver.HttpServer;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.io.OutputStream;

public class Main {
    static final String PAGE = """
    <!DOCTYPE html><html><head>
    <title>Temperature and Timer</title>
    <meta name="viewport" content="width=device-width">
    <style>
    body{font:18px Arial;max-width:650px;margin:35px auto;padding:15px;background:#eef2f7}
    main{background:white;padding:24px;border-radius:12px}
    input,select,button{padding:10px;margin:6px}
    button{cursor:pointer}
    section{padding:15px;background:#f3f4f6;margin:12px 0;border-radius:8px}
    </style></head><body><main>
    <h1>Temperature Converter</h1>
    <section>
      <input id="temp" type="number" step="any" value="25">
      <select id="unit"><option value="C">Celsius</option><option value="F">Fahrenheit</option></select>
      <button onclick="convert()">Convert</button>
      <p id="converted"></p>
    </section>
    <h1>Stopwatch</h1>
    <section>
      <h2 id="clock">00:00</h2>
      <button onclick="start()">Start</button>
      <button onclick="stop()">Stop</button>
      <button onclick="reset()">Reset</button>
    </section>
    <script>
    function convert(){
      let v=Number(temp.value);
      if(temp.value===''){converted.textContent='Enter a temperature';return;}
      converted.textContent=unit.value==='C'
        ?v+' °C = '+(v*9/5+32).toFixed(2)+' °F'
        :v+' °F = '+((v-32)*5/9).toFixed(2)+' °C';
    }
    let seconds=0,interval=null;
    function display(){
      clock.textContent=String(Math.floor(seconds/60)).padStart(2,'0')
        +':'+String(seconds%60).padStart(2,'0');
    }
    function start(){
      if(interval===null)interval=setInterval(()=>{seconds++;display()},1000);
    }
    function stop(){clearInterval(interval);interval=null;}
    function reset(){stop();seconds=0;display();}
    </script></main></body></html>
    """;

    static void send(com.sun.net.httpserver.HttpExchange ex,
                     String type,String body)throws java.io.IOException{
        byte[] b=body.getBytes(StandardCharsets.UTF_8);
        ex.getResponseHeaders().set("Content-Type",type+"; charset=UTF-8");
        ex.sendResponseHeaders(200,b.length);
        try(OutputStream os=ex.getResponseBody()){os.write(b);}
    }
    public static void main(String[] args)throws Exception{
        int port=Integer.parseInt(System.getenv().getOrDefault("PORT","8080"));
        HttpServer server=HttpServer.create(new InetSocketAddress(port),0);
        server.createContext("/api/health",ex->
            send(ex,"application/json","{\"status\":\"ok\",\"app\":\"temperature-timer\"}"));
        server.createContext("/",ex->send(ex,"text/html",PAGE));
        server.start();
        System.out.println("Temperature and timer app running on "+port);
    }
}
