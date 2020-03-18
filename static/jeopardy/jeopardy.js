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
    if (e.data != "I'm alive!") {
        console.log(e.data + " buzzed in!");
        var sounds = document.getElementsByTagName('audio');
        for (i = 0; i < sounds.length; i++) sounds[i].pause();
        httpGetAsync('/jeopardy/buzzedin?name=False,RESET');
        if (document.getElementById('id02').style.display == 'none' || document.getElementById('id02').style.display == '') {
            document.getElementById('id02').style.display = 'block';
            document.getElementById('modalcontent').innerHTML = "<h3 style=text-align:center;>" + e.data + " buzzed in! </h3>"
        }
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

function newfinal() {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            var final = xmlHttp.responseText;
        var temp = '<audio controls preload="none"><source src="/jeopardy/song?song={{song}}" /></audio>';
        console.log()
        temp = temp.replace("{{song}}", final);
        final = final.split("\\");
        final = final[final.length - 1];
        final = final.replace(".m4a", "");
        temp = temp.replace("{{song(clean)}}", final)
        var answer = document.createElement('h5');
        answer.innerHTML = final;
        answer.id = 'final';
        answer.style = 'display:none';
        document.getElementById('final_jeopardy').innerHTML = temp;
        oldfinalanswer=document.getElementById('final');
        if (oldfinalanswer!=null){
        oldfinalanswer.parentNode.removeChild(oldfinalanswer);
        }
        document.getElementsByClassName('w3-modal-content')[0].appendChild(answer);
    }
    xmlHttp.open("GET", "/jeopardy/final", true); // true for asynchronous 
    xmlHttp.send(null);
}
function getresponses() {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            var responses = xmlHttp.responseText;
        if (responses != undefined) {
            console.log(responses);
            document.getElementById('id02').style.display = 'block';
            responses = responses.split('\n');
            var start = "<table style='table-layout: fixed;'><tr>";
            var names = "";
            var wagers = "";
            var answers = "";
            responses.forEach(player => {
                if (player != "") {
                    console.log(player);
                    player = player.split(',');
                    names = names + "<th><h3>" + player[0] + "<h3></th>";
                    wagers = wagers + "<td><button class='w3-theme-dark-element w3-button w3-round' onclick='add_final_wager({{name}},{{wager}})'>+</button><h4>" + player[1] + "</h4><button class='w3-theme-dark-element w3-button w3-round' onclick='add_final_wager({{name}},-{{wager}})'>-</button></td>";
                    wagers=wagers.replace(/{{name}}/g,'"'+player[0]+'"');
                    wagers=wagers.replace(/{{wager}}/g,player[1]);
                    answers = answers + "<td><h4>" + player[2] + "</h4></td>";
                }
            });
            var end = "</tr></table>"
            document.getElementById('modalcontent').innerHTML = start + names + "</tr><tr>" + wagers + "</tr><tr>" + answers + "</tr><tr>" + end + '<button class="w3-theme-dark-element w3-button w3-round" onclick=show_hide("final");>Reveal answer</button><button class="w3-theme-dark-element w3-button w3-round" onclick=show_winner();>Reveal Winner</button>';
        }
    }
    xmlHttp.open("GET", "/jeopardy/finalresponses", true); // true for asynchronous 
    xmlHttp.send(null);
}
function add_final_wager(name, wager) {
    console.log(wager);
    scores[name] = scores[name] + parseInt(wager);
}
function show_hide(id) {
    var x = document.getElementById(id);
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}
var scores = {};
function incrementpoints(id, plusorminus) {
    scoredisplay = document.getElementById("currentscore" + id).innerHTML;
    if (plusorminus == '+') {
        scores[id] = parseInt(scoredisplay) + 100;
        scoredisplay = parseInt(scoredisplay) + 100;
    } else {
        scores[id] = parseInt(scoredisplay) - 100;
        scoredisplay = parseInt(scoredisplay) - 100;
    }
    document.getElementById("currentscore" + id).innerHTML = scoredisplay;
}
function show_winner(){
    var keys = Object.keys(scores)
    var values=Object.values(scores)
    var table="<table>";
    var master=[]
    for (let index = 0; index < keys.length; index++) {
        master.push([keys[index],values[index]])
    }
    master.sort((a,b)=>a[1].toString().localeCompare(b[1]));
    master.reverse();
    console.log(master)
    for (let index = 0; index < master.length; index++) {
        table=table+"<tr><th><h3>"+master[index][0]+"</h3></th><td><h5>"+master[index][1]+"</h5></td></tr>"
    }
    table=table+"</table>"
    document.getElementById("modalcontent").innerHTML=table
}