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
    messageObject.appendChild(document.createTextNode(message));
    messageList.appendChild(messageObject);
    messageList.appendChild(lineBreak);
}