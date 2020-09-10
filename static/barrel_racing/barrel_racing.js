//I stole, ahem, borrowed this from https://stackoverflow.com/questions/12232304/how-to-implement-server-push-in-flask-framework
//var current_number = document.getElementById("current_number");
//var plushidden = document.getElementById("plushidden");
//var minushidden = document.getElementById("minushidden");
var currentNumberEventSource = new EventSource("/barrelracing/counter/stream");
currentNumberEventSource.onmessage = function (e) {
    if (document.getElementById("current_number") != document.activeElement) {
        document.getElementById("current_number").value = e.data;
        document.getElementById("plushidden").value = Number(e.data) + 5;
        document.getElementById("minushidden").value = Number(e.data) - 5;
    }
    calculate_time();
};
var bestTimeEventSource = new EventSource("/barrelracing/best_time/stream");
bestTimeEventSource.onmessage = function (e) {
        document.getElementById("best_time").value = e.data;
};
var horseRateEventSource = new EventSource("/barrelracing/horse_rate/stream");
horseRateEventSource.onmessage = function (e) {
    seconds_per_horse = e.data;
    calculate_time();
    document.getElementById("current_rate").value = seconds_per_horse;
};
var seconds_per_horse = 20;
function calculate_time(){
    var rider_number = document.getElementById("rider_number").value;
    var current_number = document.getElementById("current_number").value;
    var difference = rider_number - current_number;
    var estimated_seconds = seconds_per_horse * difference;
    var estimated_minutes = estimated_seconds/60;
    document.getElementById("time_estimate").innerHTML = Math.round(estimated_minutes); 
}
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
