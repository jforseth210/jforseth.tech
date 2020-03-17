function onlyPlayOneIn(container) {
    container.addEventListener("play", function (event) {
        audio_elements = container.getElementsByTagName("audio")
        for (i = 0; i < audio_elements.length; i++) {
            audio_element = audio_elements[i];
            if (audio_element !== event.target) {
                audio_element.pause();
            }
        }
    }, true);
}

document.addEventListener("DOMContentLoaded", function () {
    onlyPlayOneIn(document.body);
});

var eventSource = new EventSource("/jeopardy/buzzerstream")
eventSource.onmessage = function (e) {
    if (e.data != "I'm alive!"){
    console.log(e.data + " buzzed in!");
    var sounds = document.getElementsByTagName('audio');
    for(i=0; i<sounds.length; i++) sounds[i].pause();
    httpGetAsync('/jeopardy/buzzedin?name=False,RESET');
    alert(e.data + " buzzed in!");
    } else {
        console.log("still connected")
    }
};
function httpGetAsync(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
    }
    xmlHttp.open("GET", theUrl, true); // true for asynchronous 
    xmlHttp.send(null);
}

function newfinal(){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            var final=xmlHttp.responseText
            var temp ='<audio controls preload="none"><source src="/jeopardy/song?song={{song}}" /></audio>';
            console.log()
            temp=temp.replace("{{song}}",final);
            document.getElementById('final_jeopardy').innerHTML=temp;
    }
    xmlHttp.open("GET", "/jeopardy/final", true); // true for asynchronous 
    xmlHttp.send(null);
}