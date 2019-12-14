function main(){
    // Get the modal
    var modal = document.getElementById("myModal");
    var templateSpot = document.getElementById("templateSpot");
    // Get the button that opens the modal
    var orderbuttons = document.getElementsByClassName("orderButton");
    for (var i = 0; i < orderbuttons.length; i++) {
      orderbuttons[i].onclick = function () {
        showModal(this);
      }
    }
    function showModal(button) {
      var temp = document.getElementById("formtemplates").contentWindow.document.querySelectorAll("template#" + button.id)[0];
      console.log(temp)
      var clon = temp.content.cloneNode(true);
      templateSpot.innerHTML = "";
      templateSpot.appendChild(clon);
      modal.style.display = "block";
    }
    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];


    // When the user clicks on <span> (x), close the modal
    span.onclick = function () {
      modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function (event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
    }
}