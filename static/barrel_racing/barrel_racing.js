//I stole, ahem, borrowed this from https://stackoverflow.com/questions/12232304/how-to-implement-server-push-in-flask-framework
//var current_number = document.getElementById("current_number");
//var plushidden = document.getElementById("plushidden");
//var minushidden = document.getElementById("minushidden");
var eventSource = new EventSource("/barrelracing/stream");
eventSource.onmessage = function (e) {
    if (current_number != document.activeElement) {
        document.getElementById("current_number").value = e.data;
        document.getElementById("plushidden").value = Number(e.data) + 1;
        document.getElementById("minushidden").value = Number(e.data) - 1;
    }
};

//This is probably the alert code.
//IDK
//W3Schools

// Get all elements with class="closebtn"
var close = document.getElementsByClassName("closebtn");
var i;

// Loop through all close buttons
for (i = 0; i < close.length; i++) {
    // When someone clicks on a close button
    close[i].onclick = function () {

        // Get the parent of <span class="closebtn"> (<div class="alert">)
        var div = this.parentElement;

        // Set the opacity of div to 0 (transparent)
        div.style.opacity = "0";

        // Hide the div after 600ms (the same amount of milliseconds it takes to fade out)
        setTimeout(function () { div.style.display = "none"; }, 600);
    }
}
