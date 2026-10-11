import com.sun.net.httpserver.HttpServer;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.io.OutputStream;

public class Main {
    static final String PAGE = """
    <!DOCTYPE html><html><head>
    <title>Java Quiz</title>
    <meta name="viewport" content="width=device-width">
    <style>
    body{font:18px Arial;max-width:650px;margin:40px auto;padding:15px;background:#eef2f7}
    main{background:white;padding:25px;border-radius:12px}
    button{padding:10px;margin:10px;cursor:pointer}
    label{display:block;padding:10px}
    </style></head><body><main>
    <h1>Java Quiz App</h1>
    <p id="progress"></p><h3 id="question"></h3>
    <div id="options"></div>
    <button id="next" onclick="next()">Submit Answer</button>
    <h2 id="result"></h2>
    <script>
    const qs=[
      {q:'Which language runs natively in a browser?',
       a:['Python','JavaScript','C'],correct:1},
      {q:'What does HTTP stand for?',
       a:['Hypertext Transfer Protocol','High Text Program','Host Transfer Page'],correct:0},
      {q:'What is 2 + 3?',
       a:['4','5','6'],correct:1}
    ];
    let index=0,score=0,answered=false;
    function show(){
      answered=false;
      progress.textContent='Question '+(index+1)+' of '+qs.length;
      question.textContent=qs[index].q;
      options.innerHTML='';
      qs[index].a.forEach((a,i)=>{
        let label=document.createElement('label');
        let radio=document.createElement('input');
        radio.type='radio';radio.name='answer';radio.value=i;
        label.append(radio,document.createTextNode(' '+a));
        options.appendChild(label);
      });
      next.textContent='Submit Answer';
    }
    function next(){
      if(index>=qs.length)return;
      if(!answered){
        let choice=document.querySelector('input[name=answer]:checked');
        if(!choice){alert('Choose an answer');return;}
        if(Number(choice.value)===qs[index].correct)score++;
        answered=true;
        nextButton();
      }else{
        index++;
        if(index===qs.length){
          question.textContent='Quiz completed!';
          options.innerHTML='';
          progress.textContent='';
          next.style.display='none';
          result.textContent='Your score: '+score+' / '+qs.length;
        }else show();
      }
    }
    function nextButton(){next.textContent='Next Question';}
    show();
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
            send(ex,"application/json","{\"status\":\"ok\",\"app\":\"quiz\"}"));
        server.createContext("/",ex->send(ex,"text/html",PAGE));
        server.start();
        System.out.println("Quiz app running on port "+port);
    }
}
