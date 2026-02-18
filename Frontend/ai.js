function sendMessage(){
 let input=document.getElementById("userInput");
 let chat=document.getElementById("chatBox");

 if(input.value==="") return;

 chat.innerHTML+=`<div class="msg user">${input.value}</div>`;

 setTimeout(()=>{
   chat.innerHTML+=`<div class="msg bot">I am analyzing your query...</div>`;
   chat.scrollTop=chat.scrollHeight;
 },600);

 input.value="";
}

function startVoice(){
 let rec = new(window.SpeechRecognition || window.webkitSpeechRecognition)();
 rec.lang="en-IN";

 rec.onresult=function(e){
   document.getElementById("userInput").value=e.results[0][0].transcript;
   sendMessage();
 }

 rec.start();
}
