//I stole, ahem, borrowed this from https://stackoverflow.com/questions/12232304/how-to-implement-server-push-in-flask-framework
var eventSource = new EventSource("/message/stream")
eventSource.onmessage = function (e) {
    //document.getElementById("messageListParent").appendChild(appendToList(e.data));
    appendToList(e.data);
};
//Based on https://stackoverflow.com/questions/11128700/create-a-ul-and-fill-it-based-on-a-passed-array
function appendToList(message) {
    /*var list = document.createElement('ul');
    for (var i = 0; i < messages.length; i++) {
        var message = document.createElement('li');
        message.classList.add("message");
        message.appendChild(document.createTextNode(messages[i]));

        list.appendChild(message);
    }
    return list;*/
    var messageList = document.getElementById("messagelist");
    var messageObject = document.createElement('li');
    var lineBreak = document.createElement('li');
    messageObject.classList.add("message");
    //This abomination is from https://stackoverflow.com/questions/6763148/how-to-show-literal-html-script-in-a-web-page#6763171
    //It's (probably) safe because I'm running createTextNode() which is just text, never interpereted as html.
    var unescaped = new DOMParser().parseFromString(todos[i][0], 'text/html').documentElement.textContent;
    messageObject.appendChild(document.createTextNode(unescaped));
    messageList.appendChild(messageObject);
    messageList.appendChild(lineBreak);
}
function load(){
    form1.reset();
    var messagelist=document.getElementById('messagelist')
    for (let index = 0; index < messagelist.children.length; index++) {
        const element = messagelist.children[index];
        element.createTextNode(element.innerHTML+"hi");
        
    }
}