function main(){
    populatetasks();
}
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
            taskparent.className = "task";
            task.appendChild(document.createTextNode(todos[i][0]));
            task.id = i;
            //task.addEventListener("click",function(){deleteTask(i);});
            taskparent.appendChild(task);
            taskgrandparent.appendChild(taskparent);
        };
    };
};