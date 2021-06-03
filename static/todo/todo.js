function deleteTask(idx) {
    document.getElementById('deletetaskid').value = idx;
    dropdown = document.getElementById("listdropdown");
}
function chooselist() {
    dropdown = document.getElementById("listdropdown");
    selection = dropdown[dropdown.selectedIndex].value;
    populatetasks(selection);
}

function populatetasks(selectedlist = "All") {
    document.getElementById("newTaskCurrentList").value = selectedlist;
    var taskgrandparent = document.getElementById("answers");
    taskgrandparent.innerHTML = '';
    taskgrandparent.addEventListener("click", function (e) {
        var tgt = e.target;
        deleteTask(parseInt(tgt.id, 10) + 1);
    });

    for (i = 0; i < todos.length; i++) {
        if (selectedlist == "All" | selectedlist == todos[i][1]) {
            var taskparent = document.createElement('div');
            var task = document.createElement("li");
            //This abomination is from https://stackoverflow.com/questions/6763148/how-to-show-literal-html-script-in-a-web-page#6763171
            //It's (probably) safe because I'm running createTextNode() which is just text, never interpereted as html.
            var unescaped = new DOMParser().parseFromString(todos[i][0], '/var/www/jforseth.tech/text/html').documentElement.textContent;
            console.log(unescaped)
            task.appendChild(document.createTextNode(unescaped));
            task.id = i;
            //task.addEventListener("click",function(){deleteTask(i);});
            taskparent.appendChild(task);
            taskgrandparent.appendChild(taskparent);
        };
    };
};
